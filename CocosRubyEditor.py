import sublime, sublime_plugin
import os, sys, time, re

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "keywords"))
import ruby_keyword

class CocosRubyEditorCommand(sublime_plugin.EventListener):

    def __init__(self):
        self.setting = None
        self.keywords = None
        self.root_block = None
        self.count = 0
        self.add_text_locations = []


    def check(self, view):
        if not view.file_name():
            return False

        fname, ext = os.path.splitext(view.file_name())
        if ext in self.setting.get("file_exts"):
            return True

        return False


    def on_activated(self, view):
        if self.setting == None:
            self.setting = sublime.load_settings("CocosRubyEditor.sublime-settings")


    def on_activated_async(self, view):
        if self.keywords == None:
            self.keywords = self.setting.get("keywords")
            if self.keywords == None:
                self.keywords = ruby_keyword.get_keywords()
                self.setting.set("keywords", self.keywords)

        if not self.check(view):
            return

        if not self.root_block:
            self.root_block = Block.parse_document(view, self.keywords)


    def parse_document(self, view, count):
        if count == self.count:
            self.root_block = Block.parse_document(view, self.keywords)
            self.add_text_locations = []


    def on_modified_async(self, view):
        if not self.check(view):
            return

        interval = self.setting.get("parse_interval", 200)

        count = self.count
        count += 1
        sublime.set_timeout_async(lambda: self.parse_document(view, count), interval)
        self.count = count


    def on_query_completions(self, view, prefix, locations):
        if not self.check(view):
            return []

        prefix_word = self.__get_block_tokens(view, locations)
        if prefix_word.endswith(":::") or prefix_word[-2:] in ("..", ".:", ":."):
            return []
        if prefix_word[-1] == ":" and prefix_word[-2] != ":":
            return []

        include_modules = self.__get_include_modules(locations)
        keyword_dict = self.__get_check_keyword_dict(include_modules)
        token_list = prefix_word.split("::")
        token_list = token_list[:-1] + token_list[-1].split(".") if "." in token_list[-1] else token_list

        class_name = None
        func_type = "sfunctions"
        if token_list[0] in keyword_dict:
            for token in token_list:
                if len(token) > 0 and token in keyword_dict:
                    keyword_dict = keyword_dict[token]
                    if isinstance(keyword_dict, str):
                        class_name = keyword_dict
                        break
        else:
            class_name = Block.get_variable_class(token_list[0], self.root_block, locations[0], self.add_text_locations, self.keywords, include_modules)
            if class_name:
                func_type = "ifunctions"

        value_list = []
        if class_name:
            if class_name in self.keywords['classes']:
                class_dict = self.keywords['classes'][class_name]
                check_dict = {}
                while class_dict:
                    for func_name, func_value in class_dict[func_type].items():
                        if func_name in check_dict:
                            continue
                        value = ("%s\tfunction(%s)" % (func_name, class_name), func_value['sublime'])
                        value_list.append(value)
                        check_dict[func_name] = True

                    if 'base_class' in class_dict:
                        class_name = class_dict['base_class']
                        class_dict = self.keywords['classes'][class_name]
                    else:
                        class_dict = None

        else:
            for k, v in keyword_dict.items():
                value_type = "module"
                if isinstance(v, str):
                    value_type = "class"
                value = (k + "\t" + value_type, k)
                value_list.append(value)

        return value_list


    def __get_check_keyword_dict(self, include_modules):

        keyword_dict = self.keywords['tree']

        for module in include_modules:
            tmp_kdict = keyword_dict
            mdl_list = module.split("::")
            for mdl in mdl_list:
                if len(mdl) > 0 and mdl in tmp_kdict:
                    tmp_kdict = tmp_kdict[mdl]

            keyword_dict.update(tmp_kdict)

        return keyword_dict


    def __get_include_modules(self, locations):
        include_modules = []
        self.add_text_locations.append(locations[0])
        if self.root_block:
            include_modules = Block.get_include_modules(self.root_block, locations[0], self.add_text_locations)
        return include_modules


    def __split_text(self, text):
        iterator = re.finditer(r"(:|\.)+", text)
        tokens = []
        start = 0
        for match in iterator:
            token = text[start:match.start()]
            if len(token) > 0:
                tokens.append(token)
            start = match.start()
        token = text[start:]
        if len(token):
            tokens.append(token)

        return tokens


    def __get_block_tokens(self, view, locations):

        start_position = locations[0] - 1

        while True:
            if start_position < 0:
                start_position = 0
                break
            if re.match("\\s", view.substr(start_position)):
                start_position += 1
                break
            start_position -= 1

        return view.substr(sublime.Region(start_position, locations[0]))


class Block:

    block_tokens = [
        ("module", "end"),
        ("class", "end"),
        ("def", "end"),
        ("do", "end"),
        ("if", "end"),
        ("unless", "end"),
        ("case", "end"),
        ("for", "end"),
        ("while", "end"),
        ("until", "end"),
    ]

    check_tokens = r"(module|class|def|do|if|unless|case|for|while|until|end)"

    skip_tokens = ("do", "if", "unless", "for", "while", "until")

    def __init__(self, type=None, begin=None, end=None):
        self.type = type
        self.begin = begin
        self.end = end if end else begin
        self.inner_blocks = []
        self.include_blocks = []
        self.variable_blocks = []
        self.name = None
        self.value = None

    def add_child(self, child):
        self.inner_blocks.append(child)

    @property
    def children(self, pad=False):
        blocks = []

        prev_end = self.begin - 1
        for iblock in self.inner_blocks:
            if pad:
                if iblock.begin > prev_end + 1:
                    pad_block = Block("", prev_end + 1, iblock.begin - 1)
                    blocks.append(pad_block)

            blocks.append(iblock)
            prev_end = iblock.end

        for iblock in self.include_blocks:
            blocks.append(iblock)

        for vblock in self.variable_blocks:
            blocks.append(vblock)

        return blocks

    def is_contains(self, position, add_text_locations):
        add_len = len(add_text_locations)
        if add_len >= 2:
            diff = add_text_locations[-1] - add_text_locations[0]
            add_len = diff if diff > add_len else add_len
        return position >= self.begin and position <= self.end + add_len

    @property
    def region(self):
        return sublime.Region(self.begin, self.end)

    def dumps(self):
        dect = {
            "type": self.type,
            "begin": self.begin,
            "end": self.end,
            "name": self.name,
            "inner_blocks": self.dumps_blocks(self.inner_blocks),
            "include_blocks": self.dumps_blocks(self.include_blocks),
        }
        return dect

    def dumps_blocks(self, blocks):
        dump_blocks = []
        for block in blocks:
            dumps = block.dumps()
            dump_blocks.append(dumps)
        return dump_blocks

    @classmethod
    def loads(cls, block_dict):
        block = Block()
        block.name = block_dict["name"]
        block.type = block_dict["type"]
        block.begin = block_dict["begin"]
        block.end = block_dict["end"]
        block.inner_blocks = cls.loads_blocks(block_dict["inner_blocks"])
        block.include_blocks = cls.loads_blocks(block_dict["include_blocks"])

        return block

    @classmethod
    def loads_blocks(cls, blocks):
        block_list = []
        for block_dict in blocks:
            block = cls.loads(block_dict)
            block_list.append(block)

        return block_list

    def debug_print(self):
        self.__debug_print()

    def __debug_print(self, depth=0):
        indent = "  ".join(["" for d in range(0, depth + 1)])
        type_str = ("%s#%s" % (self.type, self.name) if self.name else self.type)
        print("%d# %s%s%s" % (depth, indent, type_str, self.region))
        for child in self.children:
            child.__debug_print(depth + 1)


    @classmethod
    def parse_document(cls, view, keywords):

        print("parse_document begin")

        document = view.substr(sublime.Region(0, view.size()))

        exclude_blocks = Block.__get_exclude_blocks(document)
        include_blocks = Block.__get_include_blocks(document)
        variable_blocks = Block.__get_variable_blocks(document, keywords)

        start_stack = []
        block_stack = []
        root_block = Block("global", 0, len(document))

        block_stack.append(root_block)

        global_tmp_varibales = []
        class_tmp_variables = []

        iterator = re.finditer(Block.check_tokens, document)
        for match in iterator:
            if Block.__is_contain_blocks(match.end(), exclude_blocks):
                continue

            if match.start() != 0 and not document[match.start()-1] in ("\n", "\r", "\t", " ", ",", ";", "("):
                continue
            if match.end() != len(document)-1 and not document[match.end()] in ("\n", "\r", "\t", " ", ",", ";", ")"):
                continue

            if len(start_stack) > 0:
                start_val = start_stack[-1]
                if match.group() == start_val["end_word"]:
                    start_stack.pop()
                    if start_val["start_word"] in Block.skip_tokens:
                        continue

                    block = block_stack.pop()
                    block.end = match.end() - 1
                    block_stack[-1].add_child(block)

#                    if "name" in start_val:
#                        block.name = start_val["name"]

                    remove_idx_list = []
                    for i, ex_block in enumerate(exclude_blocks):
                        if ex_block.begin > block.begin and ex_block.end < block.end:
                            block.add_child(ex_block)
                            remove_idx_list.append(i)

                    remove_idx_list.reverse()
                    [exclude_blocks.pop(i) for i in remove_idx_list]

                    remove_idx_list = []
                    for i, inc_block in enumerate(include_blocks):
                        if inc_block.begin > block.begin and inc_block.end < block.end:
                            if block.type in ("class", "module"):
                                inc_block.begin = block.begin
                                inc_block.end = block.end
                            else:
                                inc_block.end = block.end
                            block.include_blocks.append(inc_block)
                            remove_idx_list.append(i)

                    remove_idx_list.reverse()
                    [include_blocks.pop(i) for i in remove_idx_list]

                    remove_idx_list = []
                    for i, var_block in enumerate(variable_blocks):
                        if var_block.begin > block.begin and var_block.end < block.end:
                            if var_block.name.startswith("$"):
                                global_tmp_varibales.append(var_block)
                            if var_block.name.startswith("@"):
                                class_tmp_variables.append(var_block)
                            else:
                                var_block.end = block.end
                                block.variable_blocks.append(var_block)
                            remove_idx_list.append(i)

                    remove_idx_list.reverse()
                    [variable_blocks.pop(i) for i in remove_idx_list]

                    if block.type == "class" and len(class_tmp_variables) > 0:
                        for tmp_block in class_tmp_variables:
                            tmp_block.begin = block.begin
                            tmp_block.end = block.end
                            block.variable_blocks.append(tmp_block)

                        class_tmp_variables.clear()

                    continue

            for block_token in Block.block_tokens:
                if match.group() == block_token[0]:
                    start_val = {
                        "start_pos": match.start(),
                        "start_word": block_token[0],
                        "end_word": block_token[1],
                    }

#                    if match.group() in ("module", "class", "def"):
#                        str_arr = []
#                        pos = match.end() + 1
#                        while True:
#                            if re.match(r"[a-zA-Z0-9_:\.]", document[pos]):
#                                break
#                            pos += 1
#
#                        while re.match(r"[a-zA-Z0-9_:\.]", document[pos]):
#                            str_arr.append(document[pos])
#                            pos += 1
#
#                        start_val["name"] = "".join(str_arr)

                    start_stack.append(start_val)

                    if not start_val["start_word"] in Block.skip_tokens:
                        block = Block(block_token[0], match.start())
                        block.name = Block.__get_name(block, document)
                        block_stack.append(block)

                    break

        while len(start_stack) > 0:
            start_val = start_stack.pop()
            block = block_stack.pop()
            block.end = root_block.end
#            if "name" in start_val:
#                block.name = start_val["name"]

            if start_val["start_word"] in Block.skip_tokens:
                continue

            for ex_block in exclude_blocks:
                ex_block.end = block.end
                block.add_child(ex_block)
            exclude_blocks.clear()

            remove_idx_list = []
            for i, inc_block in enumerate(include_blocks):
                if block.type in ("class", "module"):
                    inc_block.end = block.end
                    block.include_blocks.append(inc_block)
                    remove_idx_list.append(i)

            remove_idx_list.reverse()
            [include_blocks.pop(i) for i in remove_idx_list]

            remove_idx_list = []
            for i, var_block in enumerate(variable_blocks):
                if var_block.name.startswith("$"):
                    continue
                if var_block.name.startswith("@") and block.type != "class":
                    continue

                var_block.end = block.end
                block.variable_blocks.append(var_block)
                remove_idx_list.append(i)

            remove_idx_list.reverse()
            [variable_blocks.pop(i) for i in remove_idx_list]

            block_stack[-1].add_child(block)

        for ex_block in exclude_blocks:
            ex_block.end = root_block.end
            root_block.add_child(ex_block)

        for inc_block in include_blocks:
            inc_block.end = root_block.end
            root_block.include_blocks.append(inc_block)

        for var_block in variable_blocks:
            var_block.end = root_block.end
            root_block.variable_blocks.append(var_block)

        for var_block in global_tmp_varibales:
            var_block.begin = root_block.begin
            var_block.end = root_block.end
            root_block.variable_blocks.append(var_block)

#        root_block.debug_print()

        print("parse_document end")

        return root_block


    @classmethod
    def get_include_modules(cls, block, position, add_text_locations):

        modules = []

        for inc_block in block.include_blocks:
            if inc_block.is_contains(position, add_text_locations):
                modules.append(inc_block.name)

        for inner_block in block.inner_blocks:
            mdls = cls.get_include_modules(inner_block, position, add_text_locations)
            modules.extend(mdls)

        return modules


    @classmethod
    def get_variable_class(cls, var_name, block, position, add_text_locations, keywords, include_modules):

        find_block = cls.__find_variable_block(var_name, block, position, add_text_locations, keywords, include_modules)

        if find_block == None:
            return None

        return cls.__get_class_name_by_func_name(find_block.value, keywords, include_modules)


    @classmethod
    def __find_variable_block(cls, var_name, block, position, add_text_locations, keywords, include_modules):
        find_block = None

        for var_block in block.variable_blocks:
            if var_block.name == var_name:
                if var_block.is_contains(position, add_text_locations):
                    find_block = var_block
                    break

        if find_block == None:
            for inner_block in block.inner_blocks:
                var_block = cls.__find_variable_block(var_name, inner_block, position, add_text_locations, keywords, include_modules)
                if var_block:
                    find_block = var_block
                    break

        while find_block:
            class_name = cls.__get_class_name_by_func_name(find_block.value, keywords, include_modules)
            if class_name in keywords['classes']:
                break

            find_block = cls.__find_variable_block(find_block.value, block, position, add_text_locations, keywords, include_modules)

        return find_block


    @classmethod
    def __get_class_name_by_func_name(cls, func_name, keywords, include_modules=None):
        word_list = func_name.split(".")
        if len(word_list) < 2:
            return None

        if word_list[0] in keywords['classes']:
            class_info = keywords['classes'][word_list[0]]
            sfunctions = class_info['sfunctions']
            for fname, fvalue in sfunctions.items():
                pos = fname.find("(")
                if pos >= 0:
                    fname = fname[:pos]

                if fname == word_list[1]:
                    return fvalue['ret_type']

        if include_modules:
            for module in include_modules:
                append_name = module + "::" + func_name
                class_name = cls.__get_class_name_by_func_name(append_name, keywords)
                if class_name:
                    return class_name

        return None


    @classmethod
    def __get_name(cls, block, document):
        if block.type in ("class", "module", "def"):
            subdoc = document[block.begin:block.end]
            name_match = re.search(r"%s\s+([a-zA-Z0-9_:\.]+)" % block.type, subdoc)
            if name_match:
                return name_match.group(1)

        return None


    @classmethod
    def __get_exclude_blocks(cls, document):

        start_pattern = r"(\"|'|#|=begin)"

        blocks = []
        iterator = re.finditer(start_pattern, document)
        for match in iterator:
            if len(blocks) > 0 and match.start() <= blocks[-1].region.end():
                continue

            btype = "comment"
            if match.group() in ('"', "'"):
                escape_cnt = Block.__get_escape_count(document, match.start() - 1)
                if escape_cnt % 2 == 1:
                    continue
                end_token = match.group()
                btype = "string"
            elif match.group() == "#":
                end_token = "\n"
            elif match.group() == "=begin":
                end_token = "=end"

            pos = -1
            start = match.start() + 1
            while True:
                pos = document.find(end_token, start)
                if pos >= 0:
                    escape_cnt = Block.__get_escape_count(document, pos - 1)
                    if escape_cnt % 2 == 1:
                        start = pos + 1
                    else:
                        break
                else:
                    break

            if pos == -1:
                pos = len(document) - 1

            block = Block(btype, match.start(), pos + len(end_token))
            blocks.append(block)

        return blocks


    @classmethod
    def __get_escape_count(cls, document, start):

        if start < 0:
            return 0

        escape_cnt = 0
        while start >= 0:
            if document[start] == "\\":
                escape_cnt += 1
                start -= 1
            else:
                break

        return escape_cnt


    @classmethod
    def __is_contain_blocks(cls, position, blocks):
        for b in blocks:
            if b.region.contains(position):
                return True
        return False


    @classmethod
    def __get_include_blocks(cls, document):
        blocks = []
        iterator = re.finditer(r"include\s+([a-zA-Z0-9_:]+)", document)
        for match in iterator:
            module_name = match.group(1)
            block = Block("include", match.start())
            block.name = module_name
            blocks.append(block)

        return blocks


    @classmethod
    def __get_variable_blocks(cls, document, keywords):
        blocks = []
        iterator = re.finditer(r"([a-zA-Z0-9_:@\.\$]+)\s*=\s*([a-zA-Z0-9_:@\.\$]+)", document)
        for match in iterator:
            if match.group(2) in ("nil", "true", "false"):
                continue
            if match.group(2)[0] in ("[", "{"):
                continue
            if re.match("^[0-9]+$", match.group(2)):
                continue

            var_name = match.group(1)
            var_value = match.group(2)

            block = Block("variable", match.start())
            block.name = var_name
            block.value = var_value
            blocks.append(block)

        return blocks

