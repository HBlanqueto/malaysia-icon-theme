project('malaysia-icon-theme', version : '0.1.0', meson_version : '>= 0.64.0')

pkg = import('pkgconfig')
pkg.generate(
  name : 'malaysia-icon-theme',
  description : 'Icon theme for the Malaysia desktop',
  dataonly : true,
)

licenses_dir = get_option('datadir') / 'licenses' / 'malaysia-icon-theme'
install_data('COPYING', install_dir : licenses_dir, install_tag : 'runtime')
install_data('COPYING_CCBYSA3', install_dir : licenses_dir, install_tag : 'runtime')
install_data('COPYING_LGPL', install_dir : licenses_dir, install_tag : 'runtime')

theme_dir = get_option('datadir') / 'icons' / 'Malaysia'
install_data('index.theme', install_dir : theme_dir, install_tag : 'runtime')

install_subdir(
  'Malaysia',
  install_dir: theme_dir,
  strip_directory : true,
  install_tag : 'runtime',
)

files('Malaysia/scalable/places/folder.svg')
if host_machine.system() == 'windows'
  install_data(
    'Malaysia/scalable/places/folder.svg',
    install_dir: theme_dir / 'scalable' / 'status',
    rename: 'folder-open.svg',
    install_tag : 'runtime',
  )
else
  install_symlink(
    'folder-open.svg',
    install_dir: theme_dir / 'scalable' / 'status',
    install_tag: 'runtime',
    pointing_to: '../places/folder.svg',
  )
endif

gtk_update_icon_cache = find_program(
  'gtk4-update-icon-cache',
  'gtk-update-icon-cache',
  required : true,
)
meson.add_install_script(
  gtk_update_icon_cache,
  '-qtf',
  get_option('prefix') / theme_dir,
  skip_if_destdir: true,
)
