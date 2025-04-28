from starlette.requests import Request


class PermissionDependency:

    def __init__(self, permission_classes: list):
        """
            permissions_classes — список Permission-классов, которые нужно проверить
        """
        self.permission_classes = permission_classes

    def __call__(self, request: Request):
        """
            Когда FastAPI вызывает зависимость, мы прогоняем все Permission'ы
        """
        for permission_class in self.permission_classes:
            permission_class(request=request)