import ruby_cocos2dx_3d_auto_keyword as cocos2dx_3d_auto
import ruby_cocos2dx_audioengine_auto_keyword as cocos2dx_audioengine_auto
import ruby_cocos2dx_auto_keyword as cocos2dx_auto
import ruby_cocos2dx_experimental_auto_keyword as cocos2dx_experimental_auto
import ruby_cocos2dx_experimental_video_auto_keyword as cocos2dx_experimental_video_auto
import ruby_cocos2dx_spine_auto_keyword as cocos2dx_spine_auto
import ruby_cocos2dx_ui_auto_keyword as cocos2dx_ui_auto

def get_keywords():

    keywords = []
    keywords.append(cocos2dx_3d_auto.get_keywords())
    keywords.append(cocos2dx_audioengine_auto.get_keywords())
    keywords.append(cocos2dx_auto.get_keywords())
    keywords.append(cocos2dx_experimental_auto.get_keywords())
    keywords.append(cocos2dx_3d_auto.get_keywords())
    keywords.append(cocos2dx_experimental_video_auto.get_keywords())
    keywords.append(cocos2dx_spine_auto.get_keywords())
    keywords.append(cocos2dx_ui_auto.get_keywords())

    all_keyword_dict = {'tree': {}, 'classes': {}}
    for keyword_dict in keywords:
        for ns, item in keyword_dict['tree'].items():
            if ns in all_keyword_dict['tree']:
                all_keyword_dict['tree'][ns].update(item)
            else:
                all_keyword_dict['tree'][ns] = item

        all_keyword_dict['classes'].update(keyword_dict['classes'])

    return all_keyword_dict

