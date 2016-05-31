# import sublime_plugin


# class MakeViewReadOnlyCommand(sublime_plugin.TextCommand):
#     def run(self, edit):
#         if self.view.file_name().endswith(".cfg"):
#             self.view.set_read_only(True)


# class ConfigFileListener(sublime_plugin.EventListener):
#     def on_load(self, view):
#         view.run_command("make_view_read_only")
