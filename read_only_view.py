import sublime
import sublime_plugin

from os.path import split as opsplit


class MakeViewReadOnlyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """Set view to read-only"""

        self.view.set_read_only(True)


class MakeViewWriteableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """Set view to writeable"""

        self.view.set_read_only(False)


class ToggleReadOnlyViewCommand(sublime_plugin.ApplicationCommand):
    def is_checked(self):
        """Returns whether "Read-Only View" menu items should be checked."""

        view = sublime.active_window().active_view()
        return view.is_read_only()

    def run(self):
        """Check if view is read-only, if so then make writeable. If not, make read-only."""

        view = sublime.active_window().active_view()
        if view.is_read_only():
            view.run_command("make_view_writeable")
        else:
            view.run_command("make_view_read_only")


class ReadOnlyFilesListener(sublime_plugin.EventListener):
    def on_load_async(self, view):
        """Every time a new view is loaded, check if its extension or filename is in settings.
           If so, set as read-only.
        """

        filename = view.file_name()
        # view hasn't been saved yet: don't worry about it
        if not filename:
            return

        s = sublime.load_settings("Read-Only View.sublime-settings")
        extensions = s.get("read_only_extensions", [])
        filenames = s.get("read_only_filenames", [])
        # if both lists are empty, don't do anything
        if not extensions and not filenames:
            return

        if extensions:
            for ext in extensions:
                if filename.endswith(ext):
                    view.run_command("make_view_read_only")

        if filenames:
            for file in filenames:
                if file == opsplit(filename)[1]:
                    view.run_command("make_view_read_only")

        # TODO: Figure out some way of matching regex file patterns
