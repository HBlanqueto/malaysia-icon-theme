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
install_data('COPYING_MIT', install_dir : licenses_dir, install_tag : 'runtime')

theme_dir = get_option('datadir') / 'icons' / 'Malaysia'
install_data('index.theme', install_dir : theme_dir, install_tag : 'runtime')

install_subdir(
  'Malaysia',
  install_dir: theme_dir,
  strip_directory : true,
  install_tag : 'runtime',
)

files('Malaysia/scalable/places/folder.svg')
# Malaysia-Dark: carpetas oscuras, hereda todo lo demás de Malaysia (tools/color/build.py)
dark_dir = get_option('datadir') / 'icons' / 'Malaysia-Dark'
install_subdir(
  'Malaysia-Dark',
  install_dir: dark_dir,
  strip_directory : true,
  install_tag : 'runtime',
)

# Malaysia-Clear and Malaysia-Clear-Dark: translucent app icons over Malaysia and Malaysia-Dark
clear_dir = get_option('datadir') / 'icons' / 'Malaysia-Clear'
clear_dark_dir = get_option('datadir') / 'icons' / 'Malaysia-Clear-Dark'
foreach variant : [['Malaysia-Clear', clear_dir], ['Malaysia-Clear-Dark', clear_dark_dir]]
  install_subdir(
    variant[0],
    install_dir: variant[1],
    strip_directory : true,
    install_tag : 'runtime',
  )
endforeach

foreach variant : [['Malaysia', theme_dir], ['Malaysia-Dark', dark_dir]]
  if host_machine.system() == 'windows'
    install_data(
      variant[0] / 'scalable' / 'places' / 'folder.svg',
      install_dir: variant[1] / 'scalable' / 'status',
      rename: 'folder-open.svg',
      install_tag : 'runtime',
    )
  else
    install_symlink(
      'folder-open.svg',
      install_dir: variant[1] / 'scalable' / 'status',
      install_tag: 'runtime',
      pointing_to: '../places/folder.svg',
    )
  endif
endforeach

gtk_update_icon_cache = find_program(
  'gtk4-update-icon-cache',
  'gtk-update-icon-cache',
  required : true,
)
foreach dir : [theme_dir, dark_dir, clear_dir, clear_dark_dir]
  meson.add_install_script(
    gtk_update_icon_cache,
    '-qtf',
    get_option('prefix') / dir,
    skip_if_destdir: true,
  )
endforeach
