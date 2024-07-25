def find_in_dict(name, name_dict, origin):
    if name in name_dict:
        if len(name_dict[name]) == 1:
            return name_dict[name][0]
        elif len(name_dict[name]) > 1:
            package_visible = [entity for entity in name_dict[name] if
                               entity.package == origin.package]
            if len(package_visible) == 1:
                return package_visible[0]
            elif len(package_visible) > 1:
                file_visible = [entity for entity in package_visible if
                                entity.file == origin.file]
                if len(file_visible) > 0:
                    return file_visible[0]
    return None
