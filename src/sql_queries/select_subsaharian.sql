/* This statement selects all individuals belonging to Subsaharian Africa.
note that the search is case-unsensitive (Africa = AfRICA)

*/
SELECT i.identificator, i.sex, p.original_name, p.region, p.working_unit, p.continent_macroarea
FROM individuals i join populations p on i.population_id=p.id
where p.continent_macroarea = 'Subsaharian AfrICA';
