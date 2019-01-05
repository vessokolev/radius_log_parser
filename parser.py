#!/usr/bin/env python3


__author__ = "Veselin Kolev"
__license__ = "GPLv2"
__version__ = "2018121900"
__maintainer__ = __author__
__email__ = "vesso.kolev@gmail.com"
__status__ = "Production"
__about__ = '''This program code parses FreeRADIUS radius.log files and,
prints out those of the lines there that contains certain
MAC address. It also supports Gzip-ed radius.log files.'''


def check_mac(string_to_check):

    '''This function verifies if the input string represents a MAC address.'''

    digits = '0123456789ABCDEF' # The hexidecimal (HEX) digits.

    MAC = ''.join([i for i in string_to_check.upper() if i in digits])

    if len(MAC) != 12: # Every MAC address is 12-digit HEX number.
                       # Return None if the string length does not
                       # match the one expected.

        return None

    else:

        return MAC     # The MAC address digits are all upper case.


def check_input(sys):

    if len(sys.argv) < 2:

        print('\n****** ERROR ******')

        print('\nInsufficient number of input parameters! Invoke the script as:\n')

        print(sys.argv[0],'MAC_ADDRESS (file)\n')

        print('where MAC_ADDRESS is 12-digit integer number representing a MAC address.' + \
              ' For example: AC128A35BB0D.\n')

        print('   * Optionally, one can specify the RADIUS log file, in FreeRADUIS log ' + \
              'format. Gzip files are also supported.\n')

        sys.exit(1)

    return None


def parse_file(sys, radiusd_log):

    use_gzip = False

    if len(sys.argv) == 3:

        radiusd_log = sys.argv[2]

        if radiusd_log[-2:].lower() == 'gz':

            use_gzip = True

            import gzip

            # Note that setting an encoding is not supported in binary mode in
            # 'open'!

            open_file = gzip.open(radiusd_log, 'rb',)

        else:

            open_file = open(radiusd_log, 'r', encoding='utf-8', errors='replace')

    else:

        open_file = open(radiusd_log, 'r', encoding='utf-8', errors='replace')


    with open_file as f_obj:

        for line in f_obj:

            if use_gzip:

                # Handle specifically the Gzip-ed files:

                line = line.decode(encoding='utf-8', errors='replace')

            if 'Auth:' in line and ' cli ' in line:

                tmp = line.split(' cli ')[1].split(')')[0]
                tmp = check_mac(tmp)

                if sys.argv[1] == tmp:

                    print(line)


if __name__ == '__main__':

    import sys

    # The default location and of the FreeRADIUS log file.
    # The default in CentOS / RHEL / Scientific Linux is:
    #
    # /var/log/radius/radius.log
    #
    # Change it accordingly, if you use different Linux distribution.
    #
    # Ths script also supports parsing Gzip-ed files.

    radiusd_log = '/var/log/radius/radius.log'

    check_input(sys)

    # Cannonize the input string to turn it into MAC:

    inp_MAC = check_mac(sys.argv[1])

    if inp_MAC is None:

        print('\nERROR!!!')
        print('\nThe input string:\n\n',sys.argv[1],'\n\ndoes not represent any valid MAC address!\n')

        sys.exit(1)

    else:

        sys.argv[1] = inp_MAC

    parse_file(sys, radiusd_log)
