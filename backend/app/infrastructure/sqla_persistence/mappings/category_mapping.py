# infrastructure/mappers/category_mapper.py
from app.db.models.category import Category as ORMCategory
from app.domain.entities.category import Category
from app.domain.value_objects.category import CategoryId, CategoryName
from app.domain.value_objects.user import UserId


def category_orm_to_entity(orm: ORMCategory) -> Category:
    return Category(
        id_=CategoryId(orm.id),
        user_id=UserId(orm.user_id),
        name=CategoryName(orm.name),
        created_at=orm.created_at,
    )


def category_entity_to_orm(entity: Category) -> ORMCategory:
    return ORMCategory(
        id=entity.id_.value,
        user_id=entity.user_id.value,
        name=entity.name.value,
        created_at=entity.created_at,
    )
