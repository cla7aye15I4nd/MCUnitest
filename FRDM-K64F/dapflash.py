import os
import sys
import tempfile


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s <elf file>" % sys.argv[0])
        sys.exit(1)
    
    else:
        path = sys.argv[1]
        
        if path.endswith('.elf'):
            fd, binpath = tempfile.mkstemp('.bin')
            
            objcopy = 'arm-none-eabi-objcopy'
            command = f'{objcopy} -O binary {path} {binpath}'

            os.system(command)
            path = binpath
        
        devpath = os.path.join('/media', os.environ['USER'], 'DAPLINK')
        if not os.path.exists(devpath):
            print('Do not find DAPLINK device')
            sys.exit(1)

        print('Flashing to DAPLINK device...')

        command = f'cp {path} {devpath}'
        os.system(command)
        