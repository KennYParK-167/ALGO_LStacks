# ABR & AVL: RECURSIVE
def emptyValues(v):
    return {"info": v, "g": None, "d": None, "h": 1}


# AVL UTILS
def get_h(n):
    return n["h"] if n is not None else 0

def get_balance(n):
    if n is None: return 0
    return get_h(n["g"]) - get_h(n["d"])

def rotation_droite(y):
    x = y["g"]
    T2 = x["d"]
    x["d"] = y
    y["g"] = T2
    y["h"] = 1 + max(get_h(y["g"]), get_h(y["d"]))
    x["h"] = 1 + max(get_h(x["g"]), get_h(x["d"]))
    return x

def rotation_gauche(x):
    y = x["d"]
    T2 = y["g"]
    y["g"] = x
    x["d"] = T2
    x["h"] = 1 + max(get_h(x["g"]), get_h(x["d"]))
    y["h"] = 1 + max(get_h(y["g"]), get_h(y["d"]))
    return y


# DEF/ INSER ABR
def inserer(n, v, mode_avl=False):
    if n is None:
        return emptyValues(v)
    
    if v < n["info"]:
        n["g"] = inserer(n["g"], v, mode_avl)
    else:
        n["d"] = inserer(n["d"], v, mode_avl)
    
    # STOP IF ABR MODE
    if not mode_avl:
        return n

    # LOG AVL
    n["h"] = 1 + max(get_h(n["g"]), get_h(n["d"]))
    balance = get_balance(n)

    if balance > 1 and v < n["g"]["info"]:
        return rotation_droite(n)
    
    if balance < -1 and v > n["d"]["info"]:
        return rotation_gauche(n)
    
    if balance > 1 and v > n["g"]["info"]:
        n["g"] = rotation_gauche(n["g"])
        return rotation_droite(n)
    
    if balance < -1 and v < n["d"]["info"]:
        n["d"] = rotation_droite(n["d"])
        return rotation_gauche(n)

    return n


# DEF/ CERCH ABR
def chercher(n, v):
    if n is None or n["info"] == v:
        return n
    if v < n["info"]:
        return chercher(n["g"], v)
    return chercher(n["d"], v)


# DEF/ SUPPR ABR
def supprimer(n, v, mode_avl=False):
    if n is None:
        return None

    if v < n["info"]:
        n["g"] = supprimer(n["g"], v, mode_avl)
    elif v > n["info"]:
        n["d"] = supprimer(n["d"], v, mode_avl)
    else:
        if n["g"] is None:
            return n["d"]
        if n["d"] is None:
            return n["g"]

        remplaçant = n["d"]
        while remplaçant["g"] is not None:
            remplaçant = remplaçant["g"]

        n["info"] = remplaçant["info"]
        n["d"] = supprimer(n["d"], remplaçant["info"], mode_avl)

    if n is None or not mode_avl:
        return n

    # EQ AVL
    n["h"] = 1 + max(get_h(n["g"]), get_h(n["d"]))
    balance = get_balance(n)

    if balance > 1 and get_balance(n["g"]) >= 0:
        return rotation_droite(n)
    if balance > 1 and get_balance(n["g"]) < 0:
        n["g"] = rotation_gauche(n["g"])
        return rotation_droite(n)
    if balance < -1 and get_balance(n["d"]) <= 0:
        return rotation_gauche(n)
    if balance < -1 and get_balance(n["d"]) > 0:
        n["d"] = rotation_droite(n["d"])
        return rotation_gauche(n)

    return n



# DEF/ ALL PARCOURS FONC
def infixe(n, liste):
    if n:
        infixe(n["g"], liste)
        liste.append(n["info"])
        infixe(n["d"], liste)

def prefixe(n, liste):
    if n:
        liste.append(n["info"])
        prefixe(n["g"], liste)
        prefixe(n["d"], liste)

def postfixe(n, liste):
    if n:
        postfixe(n["g"], liste)
        postfixe(n["d"], liste)
        liste.append(n["info"])



# DEF/ MIN & MAX FOUND
def trouver_min(n):
    if n is None: return None
    if n["g"] is None: return n["info"]
    return trouver_min(n["g"])

def trouver_max(n):
    if n is None: return None
    if n["d"] is None: return n["info"]
    return trouver_max(n["d"])

# DEF/ SUCC
def trouver_successeur(n, v):
    curr = n
    succ = None
    while curr is not None:
        if v < curr["info"]:
            succ = curr
            curr = curr["g"]
        else:
            curr = curr["d"]
    return succ["info"] if succ else None


# DEF/ SCHEMES
def dessiner(n, espaces="", est_gauche=True, est_debut=True):
    if n is None:
        return

    if est_debut:
        print(f"Sommet : {n['info']} (H={get_h(n)})")
    else:
        trait = "├── (G) " if est_gauche else "└── (D) "
        print(espaces + trait + str(n["info"]) + f" (H={get_h(n)})")

    suite_espaces = espaces + ("│   " if not est_debut and est_gauche else "    ")

    if n["g"] or n["d"]:
        dessiner(n["g"], suite_espaces, True, False)
        dessiner(n["d"], suite_espaces, False, False)



# DEF/ IMBRIQUE ALL
def lancer_tests():
    mon_arbre = None
    
    print("./ MENU")
    choix_mode = input("Voulez vous utiliser quelle mode ? ABR ou AVL : ").upper()
    is_avl = (choix_mode == "AVL")
    print(f"Mode : {'AVL' if is_avl else 'ABR'}\n")


    print("./ INSERTION")
    while True:
        try:
            saisie = int(input("Entrer une insertion (0 pour arreter) : "))
            if saisie == 0:
                break
            mon_arbre = inserer(mon_arbre, saisie, mode_avl=is_avl)
        except ValueError:
            print("Erreur : Entrer un nombre entier.")
        
        
    if mon_arbre is not None:
        print(f"\nValeur min : {trouver_min(mon_arbre)}")
        print(f"Valeur max : {trouver_max(mon_arbre)}")
        racine_val = mon_arbre["info"]
        succ_val = trouver_successeur(mon_arbre, racine_val)
        print(f"Successeur du sommet  (Sommet : {racine_val}) : {succ_val if succ_val else 'Aucun'}")

    print("\nArbre initial :")
    if mon_arbre is None:
        print("[L'arbre est vide]")
    else:
        dessiner(mon_arbre)
        
        # PARCOURS
        res_in, res_pre, res_post = [], [], []
        infixe(mon_arbre, res_in)
        prefixe(mon_arbre, res_pre)
        postfixe(mon_arbre, res_post)
        print(f"\nInfixe  : {res_in}")
        print(f"Postfixe: {res_post}")
        print(f"Préfixe : {res_pre}")
        
    
    if mon_arbre is not None:
        print("\n\n./ RECHERCHE")
        while True:
            choix_ch = input("Rechercher un chiffre ? (O/N) : ")
            if choix_ch.upper() == "N":
                break
            elif choix_ch.upper() == "O":
                try:
                    numCh = int(input("Rechercher : "))
                    trouve = chercher(mon_arbre, numCh)
                    print(f"{numCh} est il present ? \n->", "Oui" if trouve else "Non")
                except ValueError:
                    print("Erreur : Entrer un nombre entier.")
            else:
                print("Repondez par O ou N.")
    
    
    if mon_arbre is not None:
        print("\n\n./ SUPPRESSION")
        while True:
            choix_sup = input("Supprimer ? (O/N) : ")
            if choix_sup.upper() == "N":
                break
            elif choix_sup.upper() == "O":
                try:
                    numSup = int(input("Supprimer : "))
                    print(f"Suppression de {numSup}.")
                    mon_arbre = supprimer(mon_arbre, numSup, mode_avl=is_avl)
                except ValueError:
                    print("Erreur : Entrer un nombre entier.")
            else:
                print("Repondez par O ou N.")

    print("\n\nLe nouvel arbre :")
    if mon_arbre is None:
        print("[L'arbre est vide]")
    else:
        dessiner(mon_arbre)
    print("\n")

lancer_tests()