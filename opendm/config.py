import argparse
import context

# parse arguments
processopts = ['resize', 'opensfm', 'slam', 'cmvs', 'pmvs',
               'odm_meshing', 'mvs_texturing', 'odm_georeferencing',
               'odm_orthophoto']


class RerunFrom(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, processopts[processopts.index(values):])


parser = argparse.ArgumentParser(description='OpenDroneMap')


def config():
    parser.add_argument('--images', '-i',
                        metavar='<string>',
                        help='Path to input images'),

    parser.add_argument('--project-path',
                        metavar='<string>',
                        help='Path to the project to process')

    parser.add_argument('--resize-to',  # currently doesn't support 'orig'
                        metavar='<integer>',
                        default=2400,
                        type=int,
                        help='resizes images by the largest side')

    parser.add_argument('--start-with', '-s',
                        metavar='<string>',
                        default='resize',
                        choices=processopts,
                        help=('Can be one of: ' + ' | '.join(processopts)))

    parser.add_argument('--end-with', '-e',
                        metavar='<string>',
                        default='odm_orthophoto',
                        choices=processopts,
                        help=('Can be one of:' + ' | '.join(processopts)))

    rerun = parser.add_mutually_exclusive_group()

    rerun.add_argument('--rerun', '-r',
                       metavar='<string>',
                       choices=processopts,
                       help=('Can be one of:' + ' | '.join(processopts)))

    rerun.add_argument('--rerun-all',
                       action='store_true',
                       default=False,
                       help='force rerun of all tasks')

    rerun.add_argument('--rerun-from',
                       action=RerunFrom,
                       metavar='<string>',
                       choices=processopts,
                       help=('Can be one of:' + ' | '.join(processopts)))

    parser.add_argument('--video',
                        metavar='<string>',
                        help='Path to the video file to process')

    parser.add_argument('--slam-config',
                        metavar='<string>',
                        help='Path to config file for orb-slam')

    parser.add_argument('--force-focal',
                        metavar='<positive float>',
                        type=float,
                        help=('Override the focal length information for the '
                              'images'))

    parser.add_argument('--force-ccd',
                        metavar='<positive float>',
                        type=float,
                        help='Override the ccd width information for the images')

    parser.add_argument('--min-num-features',
                        metavar='<integer>',
                        default=4000,
                        type=int,
                        help=('Minimum number of features to extract per image. '
                              'More features leads to better results but slower '
                              'execution. Default: %(default)s'))

    parser.add_argument('--matcher-threshold',
                        metavar='<percent>',
                        default=2.0,
                        type=float,
                        help=('Ignore matched keypoints if the two images share '
                              'less than <float> percent of keypoints. Default:'
                              ' %(default)s'))

    parser.add_argument('--matcher-ratio',
                        metavar='<float>',
                        default=0.6,
                        type=float,
                        help=('Ratio of the distance to the next best matched '
                              'keypoint. Default: %(default)s'))

    parser.add_argument('--matcher-neighbors',
                        type=int,
                        metavar='<integer>',
                        default=8,
                        help='Number of nearest images to pre-match based on GPS '
                             'exif data. Set to 0 to skip pre-matching. '
                             'Neighbors works together with Distance parameter, '
                             'set both to 0 to not use pre-matching. OpenSFM '
                             'uses both parameters at the same time, Bundler '
                             'uses only one which has value, prefering the '
                             'Neighbors parameter. Default: %(default)s')

    parser.add_argument('--matcher-distance',
                        metavar='<integer>',
                        default=0,
                        type=int,
                        help='Distance threshold in meters to find pre-matching '
                             'images based on GPS exif data. Set to 0 to skip '
                             'pre-matching. Default: %(default)s')

    parser.add_argument('--opensfm-processes',
                        metavar='<positive integer>',
                        default=context.num_cores,
                        type=int,
                        help=('The maximum number of processes to use in dense '
                              'reconstruction. Default: %(default)s'))

    parser.add_argument('--mesh-size',
                        metavar='<positive integer>',
                        default=100000,
                        type=int,
                        help=('The maximum vertex count of the output mesh '
                              'Default: %(default)s'))

    parser.add_argument('--mesh-octree-depth',
                        metavar='<positive integer>',
                        default=9,
                        type=int,
                        help=('Oct-tree depth used in the mesh reconstruction, '
                              'increase to get more vertices, recommended '
                              'values are 8-12. Default: %(default)s'))

    parser.add_argument('--mesh-samples',
                        metavar='<float >= 1.0>',
                        default=1.0,
                        type=float,
                        help=('Number of points per octree node, recommended '
                              'and default value: %(default)s'))

    parser.add_argument('--mesh-solver-divide',
                        metavar='<positive integer>',
                        default=9,
                        type=int,
                        help=('Oct-tree depth at which the Laplacian equation '
                              'is solved in the surface reconstruction step. '
                              'Increasing this value increases computation '
                              'times slightly but helps reduce memory usage. '
                              'Default: %(default)s'))

    parser.add_argument('--texturing-data-term',
                        metavar='<string>',
                        default='gmi',
                        help=('Data term: [area, gmi]. Default: '
                              '%(default)s'))

    parser.add_argument('--texturing-outlier-removal-type',
                        metavar='<string>',
                        default='none',
                        help=('Type of photometric outlier removal method: ' 
                              '[none, gauss_damping, gauss_clamping]. Default: '  
                              '%(default)s'))

    parser.add_argument('--texturing-skip-visibility-test',
                        action='store_true',
                        default=False,
                        help=('Skip geometric visibility test. Default: '
                              ' %(default)s'))

    parser.add_argument('--texturing-skip-global-seam-leveling',
                        action='store_true',
                        default=False,
                        help=('Skip global seam leveling. Useful for IR data.'
                              'Default: %(default)s'))

    parser.add_argument('--texturing-skip-local-seam-leveling',
                        action='store_true',
                        default=False,
                        help='Skip local seam blending. Default:  %(default)s')

    parser.add_argument('--texturing-skip-hole-filling',
                        action='store_true',
                        default=False,
                        help=('Skip filling of holes in the mesh. Default: '
                              ' %(default)s'))

    parser.add_argument('--texturing-keep-unseen-faces',
                        action='store_true',
                        default=False,
                        help=('Keep faces in the mesh that are not seen in any camera. ' 
                              'Default:  %(default)s'))

    parser.add_argument('--gcp',
                        metavar='<path string>',
                        default=None,
                        help=('path to the file containing the ground control '
                              'points used for georeferencing.  Default: '
                              '%(default)s. The file needs to '
                              'be on the following line format: \neasting '
                              'northing height pixelrow pixelcol imagename'))

    parser.add_argument('--use-exif',
                        action='store_true',
                        default=False,
                        help=('Use this tag if you have a gcp_list.txt but '
                              'want to use the exif geotags instead'))

    # Depreciated
    parser.add_argument('--odm_georeferencing-useGcp',
                        action='store_true',
                        default=False,
                        help='Enabling GCPs from the file above. The GCP file '
                             'is not used by default.')

    parser.add_argument('--orthophoto-resolution',
                        metavar='<float > 0.0>',
                        default=20.0,
                        type=float,
                        help=('Orthophoto ground resolution in pixels/meter'
                              'Default: %(default)s'))

    parser.add_argument('--zip-results',
                        action='store_true',
                        default=False,
                        help='compress the results using gunzip')

    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        default=False,
                        help='Print additional messages to the console\n'
                             'Default: %(default)s')

    parser.add_argument('--time',
                        action='store_true',
                        default=False,
                        help='Generates a benchmark file with runtime info\n'
                             'Default: %(default)s')

    return parser.parse_args()