<?php session_start(); ?>
<!DOCTYPE html>
<html>
    <head>
        <title>Hydrosharks : équipe</title>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="css/style.css"/>
        <link rel="stylesheet" href="css/sponsor.css"/>
    </head>
    <body>
        <?php include("php/entete.php"); ?>
        <?php include("php/menus.php"); ?>

        <h1>Nos Sponsor</h1>
        <?php $bdd = new PDO('mysql:host=127.0.0.1;dbname=Hydroserv', 'superuser', '123');
	 
        $reqSponsor = $bdd->query('SELECT * FROM Sponsor'); 
        $nbSponsor=$reqSponsor->rowCount();?>
        <table class="sponsorTab" align="center" style="
            margin-top: 2%;
            background-color: rgb(51, 51, 59);
            border-collapse: collapse;">
            <?php
            while($donnees=$reqSponsor->fetch()){
            ?>
                <tr>
                    <td align="center">
                        <a href="<?php echo $donnees['siteweb']; ?>"  title="<?php echo $donnees['entreprise'];?>"  target="_blank"> <img src="<?php echo $donnees['logo']; ?>" height="200"> </a>
                    </td>
                    <td>
                        <p style="color:white;"> <?php echo $donnees['commentaire']; ?> </p>
                    </td>
                </tr> 
            <?php } $reqSponsor->closeCursor();?>
            </table>
        <h1>Ils nous font confiance, faites de même</h1>


        <?php include("php/piedpage.php"); ?>
    </body>

</html>