CREATE OR REPLACE VIEW v_suivi_affaires AS
SELECT
    a.id AS affaire_id,
    a.numero_affaire,
    a.client,
    a.budget_heures,

    COALESCE(SUM(p.heures), 0) AS heures_consommees,

    (a.budget_heures - COALESCE(SUM(p.heures), 0)) AS heures_restantes

FROM affaires a
LEFT JOIN pointages p ON p.affaire_id = a.id

GROUP BY
    a.id,
    a.numero_affaire,
    a.client,
    a.budget_heures;
