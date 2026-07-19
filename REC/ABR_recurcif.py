# ABR: RECURSIVE
def emptyValues(v):
    return {"info": v, "g": None, "d": None}


# DEF/ INSER FUNC
def inserer(n, v):
    if n is None:
        return emptyValues(v)
    
    if v < n["info"]:
        n["g"] = inserer(n["g"], v)
    else:
        n["d"] = inserer(n["d"], v)
    
    return n


# DEF/ CHERCH FUNC
def chercher(n, v):
    if n is None or n["info"] == v:
        return n
    
    if v < n["info"]:
        return chercher(n["g"], v)
    return chercher(n["d"], v)


# DEF/ SUP FUNC
def supprimer(n, v):
    if n is None:
        return None

    if v < n["info"]:
        n["g"] = supprimer(n["g"], v)
    elif v > n["info"]:
        n["d"] = supprimer(n["d"], v)
    else:
        if n["g"] is None:
            return n["d"]
        if n["d"] is None:
            return n["g"]

        remplaçant = n["d"]
        while remplaçant["g"] is not None:
            remplaçant = remplaçant["g"]

        n["info"] = remplaçant["info"]
        n["d"] = supprimer(n["d"], remplaçant["info"])

    return n


# DEF/ SCEHEMES INIT
def dessiner(n, espaces="", est_gauche=True, est_debut=True):
    if n is None:
        return

    if est_debut:
        print(f"Sommet : {n['info']}")
    else:
        trait = "├── (G) " if est_gauche else "└── (D) "
        print(espaces + trait + str(n["info"]))

    # DECAL PREDICT
    suite_espaces = espaces + ("│   " if not est_debut and est_gauche else "    ")

    if n["g"] or n["d"]:
        dessiner(n["g"], suite_espaces, True, False)
        dessiner(n["d"], suite_espaces, False, False)


# DEF/ TEST LAUNCH
def lancer_tests():
    mon_arbre = None
    
    chiffres = [50, 30, 70, 20, 40, 60, 80]
    for c in chiffres:
        mon_arbre = inserer(mon_arbre, c)
        
    print("Arbre initial :")
    dessiner(mon_arbre)
    
    numCh = int(input("\n\nRechercher : "))
    trouve = chercher(mon_arbre, numCh)
    print(f"{numCh} est il present ? \n->", "Oui" if trouve else "Non")
    
    numSup = int(input("\n\nSupprimer : "))
    print(f"Suppression de {numSup}.")
    mon_arbre = supprimer(mon_arbre, numSup)
    
    print("\n\nLa nouvelle arbre :")
    dessiner(mon_arbre)
    print("\n")

lancer_tests()