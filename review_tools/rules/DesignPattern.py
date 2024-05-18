from review_tools.rules.Design import StrategyPattern, TemplateMethodPattern, \
    BuilderPattern, ProxyPattern, SingletonPattern, AdapterPattern

pattern_dict = {'template': TemplateMethodPattern, 'strategy': StrategyPattern,
                'builder': BuilderPattern, 'proxy': ProxyPattern,
                'singleton': SingletonPattern, 'adapter': AdapterPattern}


def find_pattern(pattern, project):
    return pattern_dict[pattern].find_pattern(project.files)
