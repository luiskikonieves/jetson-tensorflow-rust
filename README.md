# jetson-tensorflow-rust

Repository for playing with all things Jetson Nano and Tensorflow, written in Rust. 

# How to Build

### Dependencies

Install the following dependencies to cross-compile the project for a Jetson Nano. 

1) Install RustUp, the Rust toolchain installer
    
    ```curl https://sh.rustup.rs -sSf | sh```

2) Install RustC Nightly Compiler

    ```rustup toolchain install nightly```
        
3) Install the C cross toolchain

    ```sudo apt-get install gcc-arm-linux-gnueabihf```
    
3) Rust ARM Architecture Cross Compilation Support

    ```rustup target add arm-unknown-linux-gnueabihf --toolchain stable```
    
4) Cargo-binutils

    ```cargo install cargo-binutils ```
    
    ```rustup component add llvm-tools-preview```
    
5) Tensorflow Libraries 

    ```sudo apt-get install pkg-config libssl-dev -y```
   
### Building

Run the following to build  the software:

    ```cargo build --release --target=arm-unknown-linux-gnueabihf```
       


