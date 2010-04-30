from PyQt4 import QtGui, QtCore

from camelot.core.utils import ugettext as _
from camelot.admin.object_admin import ObjectAdmin
from camelot.view.controls.editors.one2manyeditor import One2ManyEditor
from user_translatable_label import UserTranslatableLabel

class Attribute(object):
    """Helper class representing a field attribute's name and its value"""
    def __init__(self, name, value):
        self.name = unicode(name)
        self.value = unicode(value)
                
    class Admin(ObjectAdmin):
        list_display = ['name', 'value']
        field_attributes = {'name':{'minimal_column_width':25},
                            'value':{'minimal_column_width':25}}
                        
class FieldLabel(UserTranslatableLabel):
    """A Label widget used to display the name of a field on a form.
    This label provides the user with the possibility to change the translation
    of the label and review its field attributes.
    """
    
    def __init__(self, field_name, text, field_attributes, admin, parent=None):
        """
        :param field_name: the name of the field
        :param text: user translatable string to be used as field label
        :param field_attributes: the field attributes associated with the field for which
        this is a label
        :param admin: the admin of the object of the field
        """
        super(FieldLabel, self).__init__(text, parent)
        show_field_attributes_action = QtGui.QAction(_('View attributes'), self)
        self.connect(show_field_attributes_action, QtCore.SIGNAL('triggered()'), self.show_field_attributes)
        self.addAction(show_field_attributes_action)
        self._field_name = field_name
        self._admin = admin
        self._field_attributes = field_attributes
        
    def get_attributes(self):
        return [Attribute(key,value) for key,value in self._field_attributes.items()]
    
    def show_field_attributes(self):
        from camelot.view.proxy.collection_proxy import CollectionProxy
                    
        admin = self._admin.get_related_entity_admin(Attribute)
        attributes_collection = CollectionProxy(admin=admin, 
                                                collection_getter=self.get_attributes,
                                                columns_getter=admin.get_columns)
        
        class FieldAttributesDialog(QtGui.QDialog):
            
            def __init__(self, field_name, parent=None):
                super(FieldAttributesDialog, self).__init__(parent)
                self.setWindowTitle(_('Field Attributes'))
                layout = QtGui.QVBoxLayout()
                layout.addWidget( QtGui.QLabel(field_name) )
                editor = One2ManyEditor(admin=admin, editable=False, parent=self)
                editor.set_value(attributes_collection)
                editor.setMinimumSize(600, 400)
                layout.addWidget(editor)
                self.setLayout(layout)
        
        dialog = FieldAttributesDialog(self._field_name, self)
        dialog.exec_()