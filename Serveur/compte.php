<?php session_start(); ?>

<!DOCTYPE html>
<html>
    <head>
        <title>Hydrosharks : Compte</title>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="css/style.css"/>
        <link rel="stylesheet" href="css/sponsor.css"/>
    </head>
    <body>
        <?php include("php/entete.php"); ?>
        <?php include("php/menus.php"); ?>


        <?php //https://www.primfx.com/tuto-php-creer-espace-membre-1-3-inscription-156/
            try{
                $bdd =new PDO('mysql:host=localhost;dbname=Hydroserv','superuser','123'); 
            }
            catch(Exception $e){
                die('Error :' . $e->getMessage());
            }   
            
            if(isset($_POST['forminscription'])) {
                $pseudo = htmlspecialchars($_POST['pseudo']); //on évite le code html dans les pseudo
                $mail = htmlspecialchars($_POST['mail']);
                $mail2 = htmlspecialchars($_POST['mail2']);
                $mdp = sha1($_POST['mdp']);
                $mdp2 = sha1($_POST['mdp2']);
                if(!empty($_POST['pseudo']) AND !empty($_POST['mail']) AND !empty($_POST['mail2']) AND !empty($_POST['mdp']) AND !empty($_POST['mdp2'])) {
                    $pseudolength = strlen($pseudo);
                    if($pseudolength <= 255) {
                        if($mail == $mail2) {
                            if(filter_var($mail, FILTER_VALIDATE_EMAIL)) {
                            $reqmail = $bdd->prepare("SELECT * FROM Membres WHERE email = ?");
                            $reqmail->execute(array($mail));
                            $mailexist = $reqmail->rowCount();
                            if($mailexist == 0) {
                                if($mdp == $mdp2) {
                                    $insertmbr = $bdd->prepare("INSERT INTO Membre (pseudo, email, mdp) VALUES(?, ?, ?)");
                                    $insertmbr->execute(array($pseudo, $mail, $mdp));
                                    $erreur = "Votre compte a bien été créé ! Connecter vous";
                                } else {
                                    $erreur = "Vos mots de passes ne correspondent pas !";
                                }
                            } else {
                                $erreur = "Adresse mail déjà utilisée !";
                            }
                            } else {
                            $erreur = "Votre adresse mail n'est pas valide !";
                            }
                        } else {
                            $erreur = "Vos adresses mail ne correspondent pas !";
                        }
                    } else {
                        $erreur = "Votre pseudo ne doit pas dépasser 255 caractères !";
                    }
                } else {
                    $erreur = "Tous les champs doivent être complétés !";
                }
            }
            ?>
            <div class="compte">
                <div class="inscription" align="center">
                    <h2>Inscription</h2>
                    <br /><br />
                    <form method="POST" action="">
                        <table>
                        <tr>
                            <td align="right">
                                <label for="pseudo">Pseudo :</label>
                            </td>
                            <td>
                                <input type="text" placeholder="Votre pseudo" id="pseudo" name="pseudo" value="<?php if(isset($pseudo)) { echo $pseudo; } ?>" />
                            </td>
                        </tr>
                        <tr>
                            <td align="right">
                                <label for="mail">Mail :</label>
                            </td>
                            <td>
                                <input type="email" placeholder="Votre mail" id="mail" name="mail" value="<?php if(isset($mail)) { echo $mail; } ?>" />
                            </td>
                        </tr>
                        <tr>
                            <td align="right">
                                <label for="mail2">Confirmation du mail :</label>
                            </td>
                            <td>
                                <input type="email" placeholder="Confirmez votre mail" id="mail2" name="mail2" value="<?php if(isset($mail2)) { echo $mail2; } ?>" />
                            </td>
                        </tr>
                        <tr>
                            <td align="right">
                                <label for="mdp">Mot de passe :</label>
                            </td>
                            <td>
                                <input type="password" placeholder="Votre mot de passe" id="mdp" name="mdp" />
                            </td>
                        </tr>
                        <tr>
                            <td align="right">
                                <label for="mdp2">Confirmation du mot de passe :</label>
                            </td>
                            <td>
                                <input type="password" placeholder="Confirmez votre mdp" id="mdp2" name="mdp2" />
                            </td>
                        </tr>
                        <tr>
                            <td></td>
                            <td align="center">
                                <br />
                                <input type="submit" name="forminscription" value="Je m'inscris" />
                            </td>
                        </tr>
                        </table>
                    </form>

                    <?php
                    if(isset($erreur)){
                        echo '<font color="red">'.$erreur."</font>";
                    }
                    ?>
                    
                </div>
                
                <div class="connexion">
                    <?php
                    $bdd = new PDO('mysql:host=127.0.0.1;dbname=Hydroserv', 'superuser', '123');
                    
                    if(isset($_POST['formconnexion'])) {
                    $mailconnect = htmlspecialchars($_POST['mailconnect']);
                    $mdpconnect = sha1($_POST['mdpconnect']);
                    echo $mailconnect;
                    echo $mdpconnect;
                    if(!empty($mailconnect) AND !empty($mdpconnect)) {
                        $requser = $bdd->prepare("SELECT * FROM Membre WHERE email = ? AND mdp = ?");
                        $requser->execute(array($mailconnect, $mdpconnect));
                        $userexist = $requser->rowCount();
                        if($userexist == 1){
                            $userinfo = $requser->fetch();
                            $_SESSION['id'] = $userinfo['id'];
                            $_SESSION['pseudo'] = $userinfo['pseudo'];
                            header("Location: profil.php");
                        }else {
                            $erreur = "Mauvais mail ou mot de passe !";
                        }
                    } else {
                        $erreur = "Tous les champs doivent être complétés !";
                    }
                    }
                    ?>


                    <h2>Connexion</h2>
                    <br /><br />
                    <form method="POST" action="">
                        <input type="email" name="mailconnect" placeholder="Mail" />
                        <input type="password" name="mdpconnect" placeholder="Mot de passe" />
                        <br /><br />
                        <input type="submit" name="formconnexion" value="Se connecter !" />
                    </form>
                    <?php
                    if(isset($erreur)) {
                        echo '<font color="red">'.$erreur."</font>";
                    }
                    ?>

	
                </div>
            </div>

        <?php include("php/piedpage.php"); ?>
    </body>
</html>
