import sublime
import sublime_plugin

from os.path import split as opsplit


class MakeViewReadOnlyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.set_read_only(True)


class MakeViewWriteableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.set_read_only(False)


class ToggleReadOnlyViewCommand(sublime_plugin.ApplicationCommand):
    def is_checked(self, view):
        """Returns whether "Read-Only View" menu items should be checked"""
        return view.is_read_only()

    def run(self, view):
        if view.is_read_only():
            view.run_command("make_view_writeable")
        else:
            view.run_command("make_view_read_only")


class ReadOnlyFilesListener(sublime_plugin.EventListener):
    def on_load_async(self, view):
        filename = view.file_name()
        if not filename:
            return

        s = view.settings("Read-Only View.sublime-settings")
        extensions = s.get("read_only_extensions", [])
        filenames = s.get("read_only_filenames", [])
        if not extensions or not filenames:
            return

        if extensions:
            for ext in extensions:
                if filename.endswith(ext):
                    view.run_command("make_view_read_only")

        if filenames:
            for file in filenames:
                if file == opsplit(filename)[1]:
                    view.run_command("make_view_read_only")
