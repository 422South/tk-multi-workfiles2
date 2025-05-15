import os
import shutil
import sgtk
from sgtk.platform.qt import QtCore, QtGui

HookClass = sgtk.get_hook_baseclass()


class HookFileNotFound(HookClass):
    """
    Hook called when a file needs to be copied
    """

    def execute(self, source_path, parent_ui, new_ctx, **kwargs):
        """
        Main hook entry point

        :source_path:   String
                        Source file path
        """

        if not os.path.exists(source_path):
            QtGui.QMessageBox.critical(
                parent_ui,
                "File doesn't exist!",
                "The file\n\n%s\n\nCould not be found to open!" % source_path,
            )
            return False
        return True
