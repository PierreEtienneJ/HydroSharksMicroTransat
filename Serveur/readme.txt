
CREATE USER 'superuser'@'localhost' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON Hydroserv.* TO 'superuser'@'localhost';
#DataBase Hydroserv

#Table Etudiant :
CREATE TABLE Etudiant(
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT, 
    nom VARCHAR(40) NOT NULL, 
    prenom VARCHAR(40) NOT NULL,
    id_equipe SMALLINT UNSIGNED NOT NULL,
    email VARCHAR(60), 
    linkedin VARCHAR(80),
    commentaire TEXT,
    CONSTRAINT fk_id_equipe FOREIGN KEY (id_equipe) REFERENCES Equipe(id),
    PRIMARY KEY (id)
)
ENGINE=INNODB;
#Electronique
INSERT INTO Etudiant(nom, prenom, id_equipe, email, linkedin, commentaire, promo) VALUES ('Josse', 'Pierre-Etienne', 3, 'pierreetiennejosse@hotmail.com' ,'https://www.linkedin.com/in/pierre-etienne-josse-52b916155/', 'Responsable Electronique', '2021');
#Design
INSERT INTO Etudiant(nom, prenom, id_equipe, linkedin, commentaire, promo) VALUES ('Robin', 'Pierre', 1, 'https://www.linkedin.com/in/pierre-robin-605981151/', 'Responsable Design', '2021');
#Meca
INSERT INTO Etudiant(nom, prenom, id_equipe, promo) VALUES ('Louis','Gautier', '2', '2022');



####################################################################
#                           Table Equipe
####################################################################
CREATE TABLE Equipe(
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT, 
    nom VARCHAR(20) NOT NULL,
    commentaire TEXT,
    PRIMARY KEY (id)
)
ENGINE=INNODB


INSERT INTO Equipe(nom, commentaire) VALUES ('design', 'L\'équipe est responsable du design du bateau, calculs des voiles, de la stabilité...');
INSERT INTO Equipe(nom, commentaire) VALUES ('mécanique','L\'équipe est responsable de l\'ensemble des parties mécanique du bateau : safran, géments...');
INSERT INTO Equipe(nom, commentaire) VALUES ('éléctronique', 'L\'équipe est responsable du design du bateau, calculs des voiles, de la stabilité...');


#Table Sponsor
CREATE TABLE Sponsor(
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    entreprise VARCHAR(50) NOT NULL,
    siteweb VARCHAR(80) NOT NULL,
    logo VARCHAR(80) NOT NULL, 
    commentaire TEXT,
    PRIMARY KEY (id)
)
ENGINE=INNODB;
INSERT INTO Sponsor(entreprise, siteweb, logo, commentaire) VALUES("SeaTech", "http://www.seatech.fr/", "img/logo/seatech.png", "SeaTech est une école d'ingéieur orienté vers le secteur maritime");
INSERT INTO Sponsor(entreprise, siteweb, logo, commentaire) VALUES("LattePanda", "https://www.lattepanda.com/", "img/logo/lattepanda.jpg", "LattePanda est un constructeur de puissant mini ordinateur ");
INSERT INTO Sponsor(entreprise, siteweb, logo) VALUES("Université Toulon-Var", "http://www.univ-tln.fr/", "img/logo/université.jpeg");
INSERT INTO Sponsor(entreprise, siteweb, logo, commentaire) VALUES("Meteomatics", "https://www.meteomatics.com/", "img/logo/meteomatics.png", "Meteomatics est une entreprise de données météo");


logo-> repertoire à partir de serveur

#Table Membre 
CREATE TABLE Membre(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT, 
    pseudo VARCHAR(255) NOT NULL, 
    email VARCHAR(255) NOT NULL,
    mdp VARCHAR(255) NOT NULL,
    root TINYINT DEFAULT 0,
    verif TINYINT DEFAULT 0,
    PRIMARY KEY (id)
)
ENGINE = InnoDB; 