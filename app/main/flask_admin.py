from flask_admin import BaseView, expose


class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom.html')
    @expose('/second_page')
    def second_page(self):
        return self.render('admin/second_page.html')