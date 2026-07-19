# ABR & AVL: FUSION
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



# DEF/ RECURSIVE
def inserer_rec(n, v, mode_avl=False):
    if n is None:
        return emptyValues(v)
    
    if v < n["info"]:
        n["g"] = inserer_rec(n["g"], v, mode_avl)
    else:
        n["d"] = inserer_rec(n["d"], v, mode_avl)
    
    if not mode_avl:
        return n

    n["h"] = 1 + max(get_h(n["g"]), get_h(n["d"]))
    balance = get_balance(n)

    if balance > 1 and v < n["g"]["info"]: return rotation_droite(n)
    if balance < -1 and v > n["d"]["info"]: return rotation_gauche(n)
    if balance > 1 and v > n["g"]["info"]:
        n["g"] = rotation_gauche(n["g"])
        return rotation_droite(n)
    if balance < -1 and v < n["d"]["info"]:
        n["d"] = rotation_droite(n["d"])
        return rotation_gauche(n)
    return n

def chercher_rec(n, v):
    if n is None or n["info"] == v: return n
    if v < n["info"]: return chercher_rec(n["g"], v)
    return chercher_rec(n["d"], v)

def supprimer_rec(n, v, mode_avl=False):
    if n is None: return None

    if v < n["info"]:
        n["g"] = supprimer_rec(n["g"], v, mode_avl)
    elif v > n["info"]:
        n["d"] = supprimer_rec(n["d"], v, mode_avl)
    else:
        if n["g"] is None: return n["d"]
        if n["g"] is None or n["d"] is None: return n["g"]

        remplaçant = n["d"]
        while remplaçant["g"] is not None:
            remplaçant = remplaçant["g"]

        n["info"] = remplaçant["info"]
        n["d"] = supprimer_rec(n["d"], remplaçant["info"], mode_avl)

    if n is None or not mode_avl: return n

    n["h"] = 1 + max(get_h(n["g"]), get_h(n["d"]))
    balance = get_balance(n)

    if balance > 1 and get_balance(n["g"]) >= 0: return rotation_droite(n)
    if balance > 1 and get_balance(n["g"]) < 0:
        n["g"] = rotation_gauche(n["g"])
        return rotation_droite(n)
    if balance < -1 and get_balance(n["d"]) <= 0: return rotation_gauche(n)
    if balance < -1 and get_balance(n["d"]) > 0:
        n["d"] = rotation_droite(n["d"])
        return rotation_gauche(n)
    return n

def infixe_rec(n, liste):
    if n:
        infixe_rec(n["g"], liste)
        liste.append(n["info"])
        infixe_rec(n["d"], liste)

def prefixe_rec(n, liste):
    if n:
        liste.append(n["info"])
        prefixe_rec(n["g"], liste)
        prefixe_rec(n["d"], liste)

def postfixe_rec(n, liste):
    if n:
        postfixe_rec(n["g"], liste)
        postfixe_rec(n["d"], liste)
        liste.append(n["info"])

def trouver_min_rec(n):
    if n is None: return None
    if n["g"] is None: return n["info"]
    return trouver_min_rec(n["g"])

def trouver_max_rec(n):
    if n is None: return None
    if n["d"] is None: return n["info"]
    return trouver_max_rec(n["d"])


# DEF/ ITERRATIVE
def inserer_iter(racine, v, mode_avl=False):
    if racine is None: return emptyValues(v)
    chemin = []
    curr = racine
    while True:
        chemin.append(curr)
        if v < curr["info"]:
            if curr["g"] is None:
                curr["g"] = emptyValues(v)
                break
            curr = curr["g"]
        else:
            if curr["d"] is None:
                curr["d"] = emptyValues(v)
                break
            curr = curr["d"]
            
    if not mode_avl: return racine

    enfant = None
    while chemin:
        curr = chemin.pop()
        if enfant is not None:
            if curr["g"] and curr["g"]["info"] == enfant_ancienne_info: curr["g"] = enfant
            elif curr["d"] and curr["d"]["info"] == enfant_ancienne_info: curr["d"] = enfant
        
        curr["h"] = 1 + max(get_h(curr["g"]), get_h(curr["d"]))
        balance = get_balance(curr)
        
        if balance > 1 and v < curr["g"]["info"]: curr = rotation_droite(curr)
        elif balance < -1 and v > curr["d"]["info"]: curr = rotation_gauche(curr)
        elif balance > 1 and v > curr["g"]["info"]:
            curr["g"] = rotation_gauche(curr["g"])
            curr = rotation_droite(curr)
        elif balance < -1 and v < curr["d"]["info"]:
            curr["d"] = rotation_droite(curr["d"])
            curr = rotation_gauche(curr)
        enfant = curr
        enfant_ancienne_info = curr["info"]
    return enfant

def chercher_iter(n, v):
    curr = n
    while curr is not None and curr["info"] != v:
        if v < curr["info"]: curr = curr["g"]
        else: curr = curr["d"]
    return curr

def supprimer_iter(racine, v, mode_avl=False):
    if racine is None: return None
    chemin, curr, parent = [], racine, None
    while curr is not None and curr["info"] != v:
        chemin.append(curr)
        parent = curr
        if v < curr["info"]: curr = curr["g"]
        else: curr = curr["d"]
    if curr is None: return racine
    
    if curr["g"] is None or curr["d"] is None:
        enfants = curr["g"] if curr["g"] is not None else curr["d"]
        if parent is None: racine = enfants
        elif parent["g"] == curr: parent["g"] = enfants
        else: parent["d"] = enfants
    else:
        chemin.append(curr)
        succ_parent = curr
        succ = curr["d"]
        while succ["g"] is not None:
            chemin.append(succ)
            succ_parent = succ
            succ = succ["g"]
        curr["info"] = succ["info"]
        if succ_parent["g"] == succ: succ_parent["g"] = succ["d"]
        else: succ_parent["d"] = succ["d"]

    if not mode_avl: return racine

    enfant = None
    while chemin:
        curr = chemin.pop()
        if enfant is not None:
            if curr["g"] and curr["g"]["info"] == enfant_ancienne_info: curr["g"] = enfant
            elif curr["d"] and curr["d"]["info"] == enfant_ancienne_info: curr["d"] = enfant
        curr["h"] = 1 + max(get_h(curr["g"]), get_h(curr["d"]))
        balance = get_balance(curr)
        if balance > 1 and get_balance(curr["g"]) >= 0: curr = rotation_droite(curr)
        elif balance > 1 and get_balance(curr["g"]) < 0:
            curr["g"] = rotation_gauche(curr["g"])
            curr = rotation_droite(curr)
        elif balance < -1 and get_balance(curr["d"]) <= 0: curr = rotation_gauche(curr)
        elif balance < -1 and get_balance(curr["d"]) > 0:
            curr["d"] = rotation_droite(curr["d"])
            curr = rotation_gauche(curr)
        enfant = curr
        enfant_ancienne_info = curr["info"]
    return enfant if enfant is not None else racine

def infixe_iter(n, liste):
    pile, curr = [], n
    while pile or curr:
        while curr:
            pile.append(curr)
            curr = curr["g"]
        curr = pile.pop()
        liste.append(curr["info"])
        curr = curr["d"]

def prefixe_iter(n, liste):
    if n is None: return
    pile = [n]
    while pile:
        curr = pile.pop()
        liste.append(curr["info"])
        if curr["d"]: pile.append(curr["d"])
        if curr["g"]: pile.append(curr["g"])

def postfixe_iter(n, liste):
    if n is None: return
    pile1, pile2 = [n], []
    while pile1:
        curr = pile1.pop()
        pile2.append(curr)
        if curr["g"]: pile1.append(curr["g"])
        if curr["d"]: pile1.append(curr["d"])
    while pile2:
        liste.append(pile2.pop()["info"])

def trouver_min_iter(n):
    if n is None: return None
    curr = n
    while curr["g"] is not None: curr = curr["g"]
    return curr["info"]

def trouver_max_iter(n):
    if n is None: return None
    curr = n
    while curr["d"] is not None: curr = curr["d"]
    return curr["info"]


def trouver_successeur(n, v):
    curr, succ = n, None
    while curr is not None:
        if v < curr["info"]:
            succ = curr
            curr = curr["g"]
        else:
            curr = curr["d"]
    return succ["info"] if succ else None

def dessiner(n, espaces="", est_gauche=True, est_debut=True):
    if n is None: return
    if est_debut:
        print(f"Sommet : {n['info']} (H={get_h(n)})")
    else:
        trait = "├── (G) " if est_gauche else "└── (D) "
        print(espaces + trait + str(n["info"]) + f" (H={get_h(n)})")
    suite_espaces = espaces + ("│   " if not est_debut and est_gauche else "    ")
    if n["g"] or n["d"]:
        dessiner(n["g"], suite_espaces, True, False)
        dessiner(n["d"], suite_espaces, False, False)




# DEF/ IMRIQUE ALL
def lancer_tests():
    mon_arbre = None
    
    print("./ CONFIGURATION")
    choix_approche = input("Vous vouller utiliser quelle configuration ? (REC / ITER) : ").upper()
    use_rec = (choix_approche == "REC")
    print(f"Configuration : {'RECURSIVE' if use_rec else 'ITERATIVE'}")
    
    
    print("\n./ MENU")
    choix_mode = input("Avec quelle mode ? ABR ou AVL : ").upper()
    is_avl = (choix_mode == "AVL")
    print(f"Mode : {'AVL' if is_avl else 'ABR'}")


    print("\n\n./ INSERTION")
    while True:
        try:
            saisie = int(input("Entrer une insertion (0 pour arreter) : "))
            if saisie == 0:
                break
            if use_rec:
                mon_arbre = inserer_rec(mon_arbre, saisie, mode_avl=is_avl)
            else:
                mon_arbre = inserer_iter(mon_arbre, saisie, mode_avl=is_avl)
        except ValueError:
            print("Erreur : Entrer un nombre entier.")
        
    if mon_arbre is not None:
        v_min = trouver_min_rec(mon_arbre) if use_rec else trouver_min_iter(mon_arbre)
        v_max = trouver_max_rec(mon_arbre) if use_rec else trouver_max_iter(mon_arbre)
        print(f"\nValeur min : {v_min}")
        print(f"Valeur max : {v_max}")
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
        if use_rec:
            infixe_rec(mon_arbre, res_in)
            prefixe_rec(mon_arbre, res_pre)
            postfixe_rec(mon_arbre, res_post)
        else:
            infixe_iter(mon_arbre, res_in)
            prefixe_iter(mon_arbre, res_pre)
            postfixe_iter(mon_arbre, res_post)
            
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
                    trouve = chercher_rec(mon_arbre, numCh) if use_rec else chercher_iter(mon_arbre, numCh)
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
                    if use_rec:
                        mon_arbre = supprimer_rec(mon_arbre, numSup, mode_avl=is_avl)
                    else:
                        mon_arbre = supprimer_iter(mon_arbre, numSup, mode_avl=is_avl)
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