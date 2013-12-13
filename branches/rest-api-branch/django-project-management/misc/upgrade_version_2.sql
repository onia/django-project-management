-- Database script to upgrade pre-ExtJS application to current version

ALTER TABLE wbs_projectphase ADD COLUMN description text NOT NULL;
ALTER TABLE wbs_projectphase ADD COLUMN stage_number integer NOT NULL;
ALTER TABLE deliverables_deliverable CHANGE COLUMN method testing_method text NOT NULL;
ALTER TABLE projects_project ADD COLUMN quality_plan text NOT NULL;
ALTER TABLE wbs_workitem ADD COLUMN project_stage_id integer NOT NULL;
-- ALTER TABLE projects_project ADD COLUMN communications_plan text NOT NULL;
CREATE TABLE `projects_project_stage_plan` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `project_id` integer NOT NULL,
    `projectstage_id` integer NOT NULL,
    UNIQUE (`project_id`, `projectstage_id`)
)
;
ALTER TABLE `projects_project_stage_plan` ADD CONSTRAINT `project_id_refs_id_85bff47` FOREIGN KEY (`project_id`) REFERENCES `projects_project` (`id`);
ALTER TABLE `projects_project_stage_plan` ADD CONSTRAINT `projectstage_id_refs_id_3f48e527` FOREIGN KEY (`projectstage_id`) REFERENCES `wbs_projectstage` (`id`);


CREATE TABLE `wbs_projectstage` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `stage` varchar(255) NOT NULL,
    `description` longtext NOT NULL,
    `stage_number` integer NOT NULL
)
;



INSERT INTO wbs_projectstage ( stage, description, id ) VALUES ( "Default", "", 1 );

UPDATE wbs_workitem SET project_stage_id = 1;
ALTER TABLE wbs_workitem DROP COLUMN project_phase_id;
ALTER TABLE files_projectfile CHANGE COLUMN type `file_type` integer NOT NULL;

ALTER TABLE projects_project ADD COLUMN `duration_type` integer NOT NULL;
ALTER TABLE wbs_workitem CHANGE COLUMN number_days duration integer;



