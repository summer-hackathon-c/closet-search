class PrimaryReplicaRouter:
    """
    書き込み → Writer
    読み取り → Replica
    ただし認証・セッション系は必ず Writer
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label in ["auth", "admin", "sessions", "contenttypes"]:
            return "default"
        return "replica"

    def db_for_write(self, model, **hints):
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"