import os
import sys

build_path = ['bin', 'build', 'target', 'debug', 'release']
target_board = ['FRDM-K64F', 'SAM3X8E', 'STM32F103RB', 'STM32F429ZI']


def make(path):
    target_path = os.path.join(path, 'target')
    if not os.path.exists(target_path):
        os.mkdir(target_path)

    path = os.path.abspath(path)

    for board in os.listdir(path):
        if board in target_board:

            board_path = os.path.join(path, board)
            for peripheral in os.listdir(board_path):                
                peripheral_path = os.path.join(board_path, peripheral)

                if os.path.isdir(peripheral_path):
                    for version in os.listdir(peripheral_path):
                        collect(path, board, peripheral, version)


def collect(origin_path, board, peripheral, version):
    cwd = os.getcwd()
    path = os.path.join(origin_path, board, peripheral, version)

    os.chdir(path)

    filenames = os.listdir(path)
    if 'Makefile' in filenames:
        os.system(f'make')
    
    elif 'build.sh' in filenames:
        os.system(f'bash build.sh')
    
    else:
        return os.chdir(cwd)

    for build in build_path:
        if build in filenames:
            target = os.path.join(path, build)
            name = f'{board}-{peripheral}-{version}.elf'
            copy_path = os.path.join(origin_path, 'target', name)
            
            os.system(f'cp {target}/*.elf {copy_path}')
            break
    
    os.chdir(cwd)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        make('.')
    else:
        make(sys.argv[1])
