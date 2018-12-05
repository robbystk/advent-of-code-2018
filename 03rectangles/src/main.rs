use std::env;
use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;
use std::collections::HashMap;

#[derive(Debug)]
struct Rectangle {
    number:     u32,
    hoffset:    u32,
    voffset:    u32,
    width:      u32,
    height:     u32,
}

impl Rectangle {
    fn from_str(s: &str) -> Rectangle {
        let num_index = s.find('#').unwrap() + 1;
        let end_num_index = s.find(" @ ").unwrap();
        let voffset_index = s.find(",").unwrap();
        let width_index = s.find(": ").unwrap();
        let height_index = s.find("x").unwrap();
        let num_str = &s[num_index..end_num_index];
        let hoffset_str = &s[(end_num_index + 3)..voffset_index];
        let voffset_str = &s[(voffset_index + 1)..width_index];
        let width_str = &s[(width_index + 2)..height_index];
        let height_str = &s[(height_index + 1)..];
        let num: u32 = num_str.parse().unwrap();
        let hoffset: u32 = hoffset_str.parse().unwrap();
        let voffset: u32 = voffset_str.parse().unwrap();
        let width: u32 = width_str.parse().unwrap();
        let height: u32 = height_str.parse().unwrap();
        return Rectangle{
            number: num,
            hoffset: hoffset,
            voffset: voffset,
            width: width,
            height: height,
        };
    }
}

fn print_counts(c: &HashMap<(u32, u32), i32>) {
    for i in 0..8 {
        for j in 0..8 {
            match c.get(&(i,j)) {
                Some(c) => print!("{}", c),
                None => print!("."),
            };
        }
        print!("\n");
    }
}

fn no_overlap(r: &Rectangle, c: &HashMap<(u32, u32), i32>) -> bool {
    for i in r.hoffset..r.hoffset+r.width {
        for j in r.voffset..r.voffset+r.height {
            if *c.get(&(i,j)).unwrap() > 1 {
                return false;
            }
        }
    }
    return true;
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let filename = &args[1];

    let f = File::open(filename).expect("file not found");

    let reader = BufReader::new(f);

    let lines: Vec<_> = reader.lines().collect();

    let mut counts = HashMap::new();

    let rectangles: Vec<_> = lines
        .into_iter()
        .map(|l| {Rectangle::from_str(&l.unwrap())})
        .collect();

    for r in &rectangles {
        for i in r.hoffset..r.hoffset+r.width {
            for j in r.voffset..r.voffset+r.height {
                let count = counts.entry((i,j)).or_insert(0);
                *count += 1;
            }
        }
    }

    // print counts
    print_counts(&counts);

    // add up doubly-covered square inches
    let mut square_inches_in_multiple_rectangles = 0;
    for c in counts.values() {
        if *c > 1 {
            square_inches_in_multiple_rectangles += 1;
        }
    }

    println!("{} square inches of fabric are part of multiple claims",
             square_inches_in_multiple_rectangles);

    // find non-overlapping claims
    for r in &rectangles {
        if no_overlap(&r, &counts) {
            println!("Claim {} overlaps with no other claims.",
                     r.number);
        }
    }
}
