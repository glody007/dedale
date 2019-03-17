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
