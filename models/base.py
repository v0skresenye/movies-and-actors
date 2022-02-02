from core import db

def commit(obj):
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)
    return obj


class Model(object):
    @classmethod
    def create(cls, **kwargs):
        """
        Create record
        """
        obj = cls(**kwargs)
        return commit(obj)

    @classmethod
    def update(cls, row_id, **kwargs):
        """
        Update record by id
        """
        obj = cls.query.filter_by(id=row_id).first()
        for key, val in kwargs.items():
            setattr(obj, key, val)
        return commit(obj)

    @classmethod
    def delete(cls, row_id):
        """
        Delete record by id
        """
        obj = cls.query.filter_by(id=row_id).delete()
        db.session.commit()
        return obj

    @classmethod
    def add_relation(cls, row_id, rel_obj):
        """
        Add relation to object
        """
        obj = cls.query.filter_by(id=row_id).first()
        if cls.__name__ == 'Actor':
            obj.filmography.append(rel_obj)
        elif cls.__name__ == 'Movie':
            obj.cast.append(rel_obj)
        return commit(obj)

    @classmethod
    def remove_relation(cls, row_id, rel_obj):
        """
        Remove certain relation
        """
        obj = cls.query.filter_by(id=row_id).first()
        if cls.__name__ == 'Actor':
            obj.filmography.remove(rel_obj)
        elif cls.__name__ == 'Movie':
            obj.cast.remove(rel_obj)
        return commit(obj)

    @classmethod
    def clear_relations(cls, row_id):
        """
        Remove all relations by id
        """
        obj = cls.query.filter_by(id=row_id).first()
        if cls.__name__ == 'Actor':
            del obj.filmography
        elif cls.__name__ == 'Movie':
            del obj.cast
        return commit(obj)