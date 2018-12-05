use std::env;
use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;

fn main() {
    let args: Vec<String> = env::args().collect();

    let filename = &args[1];

    let f = File::open(filename).expect("file not found");

    let mut reader = BufReader::new(f);

    let lines: Vec<_> = reader.lines().collect();

    for l in lines {
        println!("{}", l.unwrap());
    }
}
