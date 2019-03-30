def dict_contient(dico_conteneur = {}, dico_contenu = {}):
    for key in dico_contenu:
        try:
            if dico_conteneur[key] != dico_contenu[key]:
                return False
        except KeyError:
            return False
    return True

def create_object_from_dico(classe, dico):
    class_rep = classe.__dict__
    instance_of_class = classe()
    instance_rep =  instance_of_class.__dict__
    for key in dico:
        if class_rep.get(key) is not None:
            instance_rep[key] = dico[key]
        else:
            raise KeyError()
    return instance_of_class

def dict_contient_keys(dico_conteneur = {}, dico_contenu = {}, requis = []):
    conteneur = dico_conteneur.keys()
    contenu = dico_contenu.keys()
    return list_contains_another(conteneur, contenu, requis)

def list_contains_another(conteneur = [], contenu = [], requis = []):
    conteneur_set = set(conteneur)
    contenu_set = set(contenu)
    requis_set = set(requis)
    if any(requis):
        return set_contains_another(conteneur_set, requis_set)
    else:
        return set_contains_another(conteneur_set, contenu_set)

def set_contains_another(conteneur = set(), contenu = set()):
    intersection = conteneur & contenu
    contenu_part_not_in_conteneur = contenu - intersection
    if any(contenu_part_not_in_conteneur):
        return False
    return True
