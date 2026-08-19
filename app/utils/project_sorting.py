from app.db.models.project import Project
from app.schemas.projects import ProjectSortField


class ProjectSort:
    sort_columns = {
        ProjectSortField.name: Project.name,
        ProjectSortField.created_at: Project.created_at,
        ProjectSortField.description: Project.description,
    }

    @classmethod
    def get_sort(
        cls,
        sort_by: ProjectSortField,
    ):
        return cls.sort_columns[sort_by]