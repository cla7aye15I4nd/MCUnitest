import os
import sys
import shutil

build_path = ['bin', 'build', 'target', 'debug', 'release']
target_board = ['FRDM-K64F', 'SAM3X8E', 'STM32F103RB', 'STM32F429ZI']
official_sdk = ['SDK', 'Arduino', 'Cube']

def make(path):
    target_path = os.path.join(path, 'target')

    other_path = os.path.join(target_path, 'other')
    official_path = os.path.join(target_path, 'official')
    
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    
    os.mkdir(target_path)
    os.mkdir(official_path)
    os.mkdir(other_path)

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

    if 'build.sh' in filenames:
        os.system(f'bash build.sh  1> /dev/null 2> /dev/null')
    
    elif 'Makefile' in filenames:
        os.system(f'make 1> /dev/null 2> /dev/null')
    
    else:
        print(f'[WARN] {path}')
        return os.chdir(cwd)

    for build in build_path:
        if build in filenames:
            name = f'{board}-{peripheral}-{version}.elf'
            where = 'official' if version in official_sdk else 'other'
            dst_path = os.path.join(origin_path, 'target', where, name)

            src_path = os.path.join(path, build)
            if version == 'RIOT':
                for sub in os.listdir(src_path):
                    src_path = os.path.join(src_path, sub)
                    break
            
            command = f'cp {src_path}/*.elf {dst_path}'
            os.system(command)
            break
    
    os.chdir(cwd)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        make('.')
    else:
        make(sys.argv[1])
