from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
try:
    from libqtile.manager import Key, Group
except ImportError:
    from libqtile.config import Key, Group

from libqtile.manager import Click, Drag, Screen

sup = "mod4"
alt = "mod1"

keys = [
 #cycle to next group left
    Key([sup], "Left", lazy.group.prevgroup()),
 # cycle to next group right
    Key([sup], "Right", lazy.group.nextgroup()),
 # Window manager controls
     Key([alt, 'control'], 'r', lazy.restart()),
     Key([alt, 'control'], 'q', lazy.shutdown()),
     Key([alt], 'r', lazy.spawn('dmenu_run')),
     Key([alt], 'Return', lazy.spawn('xterm')),
     Key([alt], 'w', lazy.window.kill()),
     Key([alt], 'Tab', lazy.layout.next()),
     Key([alt], 'Left', lazy.screen.prevgroup()),
     Key([alt], 'Right', lazy.screen.nextgroup()),
# Layout modification
     Key([alt, 'control'], 'space', lazy.window.toggle_floating()),
# Switch between windows in current stack pane
     Key([alt], "k", lazy.layout.down()),
     Key([alt], "j", lazy.layout.up()),
     Key([alt, "shift"], "k", lazy.layout.shuffle_down()),
     Key([alt, "shift"], "j", lazy.layout.shuffle_up()),
     Key([alt], "i", lazy.layout.grow()),
     Key([alt], "m", lazy.layout.shrink()),
     Key([alt], "n", lazy.layout.normalize()),  
     Key([alt], "o", lazy.layout.maximize()),
     Key([alt, "shift"], "space", lazy.layout.flip()),
     Key([alt], 'space', lazy.layout.next()),
# Toggle between different layouts as defined below
     Key([alt], 'Tab', lazy.nextlayout())
]

mouse = [
    Drag([alt], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([alt], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([alt], "Button2", lazy.window.bring_to_front())
]

# Next, we specify group names, and use the group position to generate
# a key binding for it.

groups = [
     Group('home'),
     Group('term'),
     Group('code'),
     Group('skype'),
     Group('browser')
]

for index, grp in enumerate(groups):

     # index is the position in the group list grp is the group object.
     # We assign each group object a set of keys based on it's
     # position in the list.

     # Eventually we will implement a function to change the name based
     # on what window is active in that group.

     keys.extend([

             # switch to group
         Key([alt], str(index+1), lazy.group[grp.name].toscreen()),

             # send to group
         Key([alt, "shift"], str(index+1), lazy.window.togroup(grp.name)),

             # swap with group
         Key([sup, "shift"], str(index+1), lazy.group.swap_groups(grp.name))
    ])


# Three simple layout instances:

layouts = [
    layout.Max(),
    layout.Stack(stacks=2),
    layout.Tile(ratio=0.25,
    border_focus="#000000",
    border_normal="#FFFFFF"
),
]


# orange text on grey background
default_data = dict(fontsize=12,
                    foreground="FF6600",
                    background="1D1D1D",
                    font="ttf-droid")

# we need a screen or else qtile won't load
screens = [
    Screen(bottom = bar.Bar([widget.GroupBox(**default_data),
                             widget.WindowName(**default_data),
                             widget.Clock(**default_data)],
                             27,))]

@hook.subscribe.client_new
def dialogs(window):
    if(window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
        window.floating = True

@hook.subscribe.client_new
def grouper(window, windows={'firefox-aurora': 'home',
                              'emacs': 'emacs',
                              'thunderbird': 'mail',
                              'urxvt': ['music', 'weechat'],
                              'skype': 'skype'}):

     """
     This function relies on the contentious feature of default arguments
     where upon function definition if the argument is a mutable datatype,
     then you are able to mutate the data held within that object.

     Current usage:

     {window_name: group_name}

     or for grouping windows to different groups you will need to have a
     list under the window-key with the order that you're starting the
     apps in.

     See the 'runner()' function for an example of using this method.

     Here:

     {window_name: [group_name1, group_name2]}

     Window name can be found via window.window.get_wm_class()
     """


     windowtype = window.window.get_wm_class()[0]

     # if the window is in our map
     if windowtype in windows.keys():

          # opening terminal applications gives
          # the window title the same name, this
          # means that we need to treat these apps
          # differently

          if windowtype != 'urxvt':
               window.togroup(windows[windowtype])
               windows.pop(windowtype)

          # if it's not on our special list,
          # we send it to the group and pop
          # that entry out the map
          else:
               try:
                    window.togroup(windows[windowtype][0])
                    windows[windowtype].pop(0)
               except IndexError:
                    pass


@hook.subscribe.startup
def runner():
     import subprocess

     """
     Run after qtile is started
     """

     # startup-script is simple a list of programs to run
     #subprocess.Popen('startup-script')

     # terminal programs behave weird with regards to window titles
     # we open them separately and in a defined order so that the
     # client_new hook has time to group them by the window title
     # as the window title for them is the same when they open

     #subprocess.Popen(['urxvt', '-e', 'ncmpcpp-opener'])
     #subprocess.Popen(['urxvt', '-e', 'weechat-curses'])

