import argparse
from utility import read_json_file

from two_type_operations import TwoTypeOperations
from symmetric import Symmetric
from asymmetric import Asymmetric


def main():
    parser = argparse.ArgumentParser(description="Entry point of the program")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-key', '--keys',
                       action='store_true',
                       help='Run key generation mode.')
    group.add_argument('-enc', '--encryption',
                       action='store_true',
                       help='Run encryption mode.')
    group.add_argument('-dec', '--decryption',
                       action='store_true',
                       help='Run decryption mode.')

    parser.add_argument('-k', '--key_length',
                        type=int,
                        default=448,
                        help='Length of the symmetric key in bits (default: 448).')

    parser.add_argument('-s', '--settings',
                        type=str,
                        default='paths.json',
                        help='Path to the setting file of the project')

    args = parser.parse_args()
    symmetric_crypto = Symmetric(args.key_length)
    settings = read_json_file(args.settings)
    asymmetric_crypto = Asymmetric(settings['private_key'], settings['public_key'])
    two_type_operate = TwoTypeOperations(settings['text_file'],
                                         settings['symmetric_key_file'], settings['encrypted_text_file'],
                                         settings['decrypted_text_file'], symmetric_crypto, asymmetric_crypto)

    if args.keys:
        two_type_operate.generate_keys()

    elif args.encryption:
        two_type_operate.encrypt_text()

    elif args.decryption:
        two_type_operate.decrypt_text()


if __name__ == "__main__":
    main()
