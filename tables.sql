USE gestion_heures;

-- EMPLOYES
CREATE TABLE IF NOT EXISTS employes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  login VARCHAR(50) UNIQUE,
  actif TINYINT(1) DEFAULT 1
);

-- AFFAIRES
CREATE TABLE IF NOT EXISTS affaires (
  id INT AUTO_INCREMENT PRIMARY KEY,
  numero_affaire VARCHAR(50) UNIQUE,
  budget_heures DECIMAL(7,2) DEFAULT 0
);

-- POINTAGES
CREATE TABLE IF NOT EXISTS pointages (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  employe_id INT,
  affaire_id INT,
  date_pointage DATE,
  heures DECIMAL(6,2),

  FOREIGN KEY (employe_id) REFERENCES employes(id),
  FOREIGN KEY (affaire_id) REFERENCES affaires(id)
);
