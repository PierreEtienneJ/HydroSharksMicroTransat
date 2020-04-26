<?php
	session_start();
    
    if(empty($_SESSION['id'])){
        header('Location: compte.php');
        exit();
    }
    else{
	$bdd = new PDO('mysql:host=127.0.0.1;dbname=Hydroserv', 'superuser', '123');
	 
	$requser = $bdd->prepare('SELECT * FROM Membre WHERE id = ?');
	$requser->execute(array($_SESSION['id']));
	$userinfo = $requser->fetch();
?>


<!DOCTYPE html>
<html>
    <head>
        <title>Hydrosharks : Compte</title>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="css/style.css"/>
    </head>
    <body>
        <?php include("php/entete.php"); ?>
        <?php include("php/menus.php"); ?>

	      <div align="center">
	         <h2>Profil de <?php echo $userinfo['pseudo']; ?></h2>
	         <br /><br />
	         Pseudo = <?php echo $userinfo['pseudo']; ?>
	         <br />
	         Mail = <?php echo $userinfo['email']; ?>
	         <br />
	         <?php
	         if(isset($_SESSION['id']) AND $userinfo['id'] == $_SESSION['id']) {
	         ?>
	         <br />
	         <a href="php/deconnexion.php">Se déconnecter</a>
	         <?php
	         }
	         ?>
            </div>

            <!--Si on est root-->
            <!------------------->
            <?php 
                if($userinfo['root']==1 and $userinfo['verif']==1){
            ?>
                <?php  //<!--Validation formulaire-->
                if(isset($_POST['Valider'])){
                    $requser = $bdd->prepare("UPDATE Membre SET verif=1 WHERE id =?");
                    $requser->execute(array($_POST['Valider']));
                }
                if(isset($_POST['Refuser'])){
                    $requser = $bdd->prepare("UPDATE Membre SET ban=1 WHERE id =?");
                    $requser->execute(array($_POST['Refuser']));
                }
                if(isset($_POST['ValiderE'])){
                        $requser = $bdd->prepare("UPDATE Membre SET verif=1 WHERE id =?");
                        $requser->execute(array($_POST['ValiderE']));
                        $requser = $bdd->prepare("UPDATE Membre SET etudiant=1 WHERE id =?");
                        $requser->execute(array($_POST['ValiderE']));
                }
                ?> 
                <div>
                <h1>Nouveau utilisateur</h1>
                <p>Permet de confirmer les nouveaux utilisateurs </p>
                <?php
                $req=$bdd->query("SELECT * FROM Membre WHERE verif=0 AND ban=0;");
                $nbNewUser= $req->rowCount();
                if($nbNewUser==0){ ?>
                    <p>Pas de nouveaux utilisateurs </p>
                <?php 
                }else{ ?>
                    <p>Il y a <?php echo $nbNewUser; ?>  nouveaux utilisateurs :</p>
                    <form method="post">
                    <?php while($donnees=$req->fetch()){?>
                        <div style="display: flex;">
                            <div>
                                <p> Pseudo : <?php echo $donnees['pseudo']; ?> Mail : <?php echo $donnees['email']; ?> </p>
                            </div>
                            <!-- On crée les boutons-->
                                <input class="ValiderE" type='submit' name="ValiderE" value="<?php echo $donnees['id']; ?>" style="background-color: green; border: 0px; color=green;"/>
                                <input class="Valider" type='submit' name="Valider" value="<?php echo $donnees['id']; ?>" style="background-color: yellow; border: 0px; color=yellow;" />
                                <input class="Refuser" type='submit' name="Refuser" value="<?php echo $donnees['id']; ?>" style="background-color: red; border: 0px; color=red;"/>
                                
                        </div>
                    <?php } ?>

                <?php } ?>
                
                </div>

            <?php }?>
            <?php 
                if($userinfo['verif']==0 and $userinfo['ban']==0){
            ?>
                <p>Veuillez attendre qu'un administrateur valide votre inscription </p>
            <?php }?>
            <?php 
                if($userinfo['ban']==1){
            ?>
                <p>Un administrateur à révoqué votre inscription </p>
            <?php } ?>
            <?php  if($userinfo['verif']==1){ ?>
                <p>Votre compte est valide</p>
            <?php }?>
            

            <!--Nouveau profil étudiant-->
            <?php if(isset($_POST['creeEtudiant'])){
                //On gère les trucs étrange //o n évite le code html
                $nom = htmlspecialchars($_POST['nom']);
                $prenom = htmlspecialchars($_POST['prenom']); 
                $mail = htmlspecialchars($_POST['mail']); 
                $idequipe = htmlspecialchars($_POST['equipe']); 
                $commentaire = htmlspecialchars($_POST['commentaire']); 
                $promo = htmlspecialchars($_POST['promo']);
                $linkedin=htmlspecialchars($_POST['linkedin']);

                if(!empty($_POST['nom']) AND !empty($_POST['prenom']) AND !empty($_POST['equipe'])){
                    $insert = $bdd->prepare("INSERT INTO Etudiant (nom, prenom, id_equipe, idMembre) VALUES(?,?,?,?)");
                    $insert->execute(array($nom, $prenom, $idequipe, $userinfo['id']));
                    
                    if(!empty($_POST['mail'])){
                        if(!filter_var($mail, FILTER_VALIDATE_EMAIL)){
                            echo "ERROR MAIL";
                        }
                        else{
                            $req = $bdd->prepare("UPDATE Etudiant SET email=? WHERE idMembre=?;");
                            $req->execute(array($mail,$userinfo['id']));
                        }
                    }

                    if(!empty($_POST['commentaire'])){
                        $req = $bdd->prepare("UPDATE Etudiant SET commentaire=? WHERE idMembre=?;");
                        $req->execute(array($commentaire,$userinfo['id']));
                    }
                    if(!empty($_POST['promo'])){
                        $req = $bdd->prepare("UPDATE Etudiant SET promo=? WHERE idMembre=?;");
                        $req->execute(array($promo,$userinfo['id']));
                    }
                    if(!empty($_POST['linkedin'])){
                        $req = $bdd->prepare("UPDATE Etudiant SET linkedin=? WHERE idMembre=?;");
                        $req->execute(array($linkedin,$userinfo['id']));
                    }
                    
                }
                else{
                    echo "ERROR";
                }
            }?>
            <?php if($userinfo['etudiant'] == 1 AND $userinfo['verif'] == 1){  // si le membre est un étudiant
                $requser = $bdd->prepare("SELECT * FROM Etudiant WHERE idMembre =?");
                $requser->execute(array($userinfo['id']));
                $ifetudiant=$requser->rowCount();
                if($ifetudiant==0){ //si il n'y a pas de profil lier au compte 
                //Gestion du formulaire de création
                ?>
                    <form method="POST" action="">
                        <table>
                        <tr> <!--Nom-->
                            <td align="right">
                                <label for="nom">Nom :<abbr title="Ce champ est obligatoire">*</abbr></label>
                            </td>
                            <td>
                                <input type="text" maxlength="100" placeholder="Nom" id="nom" name="nom" value="<?php if(isset($nom)) { echo $nom; } ?>" />
                            </td>
                        </tr>
                        <tr> <!--Prenom-->
                            <td align="right">
                                <label for="prenom">Prenom :<abbr title="Ce champ est obligatoire">*</abbr></label>
                            </td>
                            <td>
                                <input type="text" maxlength="100" placeholder="Prenom" id="prenom" name="prenom" value="<?php if(isset($prenom)) { echo $prenom; } ?>" />
                            </td>
                        </tr>
                        <tr><!--mail-->
                            <td align="right">
                                <label for="mail">Mail :</label>
                            </td>
                            <td>
                                <input type="email" placeholder="Votre mail" id="mail" name="mail" />
                            </td>
                        </tr>
                        <tr><!--equipe-->
                            <td align="right">
                                <label for="equipe">Equipe :<abbr title="Ce champ est obligatoire">*</abbr></label>
                            </td>
                            <td>
                                <?php $req=$bdd->query("SELECT * FROM Equipe;"); ?>
                                <select id="equipe" name="equipe" required>
                                    <?php while($donnees=$req->fetch()){?>
                                        <option value="<?php echo $donnees['id'];?>"> <?php echo $donnees['nom'];?> </option>
                                    <?php } ?>
                                </select>
                            </td>
                        </tr>
                        <tr><!--linkedin-->
                            <td align="right">
                                <label for="linkedin">Linkedin :</label>
                            </td>
                            <td>
                                <input type="text" placeholder="Votre profil linkedin" id="linkedin" name="linkedin" value="<?php if(isset($linkedin)) { echo $linkedin; } ?>" />
                            </td>
                        </tr>
                        <tr><!--commentaire-->
                            <td align="right">
                                <label for="commentaire">Contribution :</label>
                            </td>
                            <td>
                                <textarea rows="7" cols="32" id="commentaire" name="commentaire" value="<?php if(isset($commentaire)) { echo $commentaire; } ?>" /> </textarea>
                            </td>
                        </tr>
                        <tr><!--promo-->
                            <td align="right">
                                <label for="promo">Promo :</label>
                            </td>
                            <td>
                                <input type="number" min="2020" max="2025" placeholder="Votre promo" id="promo" name="promo" value="<?php if(isset($promo)) { echo $promo; } ?>" />
                            </td>
                        </tr>
                        <tr>
                            <td></td>
                            <td align="center">
                                <br />
                                <input type="submit" name="creeEtudiant" value="Je crée mon compte étudiant" />
                            </td>
                        </tr>
                        </table>
                    </form>
                <?php
                }else{  //proposer de modifier le profil?>
                    <p> Modifier Profil </p>
                    
                <?php
                }
                ?> 
                <!--Le but est de pouvoir crée et modifier son profil-->


            <?php } ?>
            <?php include("php/piedpage.php"); ?>
	   </body>
	</html>
<?php } ?>