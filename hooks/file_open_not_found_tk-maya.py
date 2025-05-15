import sgtk
import os
import maya.cmds as cmds

HookBaseClass = sgtk.get_hook_baseclass()


class HookFileNotFound(HookBaseClass):
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
            # Ask the user if they want to look on the cloud, only look if it's an asset not a shot

            confirmResult = cmds.confirmDialog(title='Confirm',
                                               message='File not found on disk\n\nDo you want to look on the cloud?',
                                               button=['Yes', 'No'], defaultButton='Yes', cancelButton='No',
                                               dismissString='No')

            if confirmResult == 'Yes':
                fw = self.parent.frameworks.get("tk-framework-422-utils")
                cloudUtils = fw.import_module('utils.cloud_utils')
                cloudUtils.downloadFromCloud(new_ctx.sgtk.shotgun, new_ctx, source_path)

        return self.parent.execute(self, source_path, parent_ui, new_ctx)
