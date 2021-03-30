use bio::io::fastq;
use rand::{Rng, RngCore, SeedableRng};
use rand_xorshift::XorShiftRng;
use std::fs::File;
use std::io;
use std::path::PathBuf;

#[derive(Debug, structopt::StructOpt)]
struct Opt {
    /// Write output to FILE; by default, output is written to the terminal (stdout)
    #[structopt(short, long)]
    outfile: Option<PathBuf>,
    /// Randomly sample N sequences from the input; by default N=500
    #[structopt(short, long, default_value = "500")]
    num_reads: usize,
    /// Seed random number generator for reproducible behavior; by default, the RNG sets its own random state
    #[structopt(short, long)]
    seed: Option<u64>,
    /// Sequences in Fastq format
    seqs: Option<PathBuf>,
}

fn main() {
    let opt = Opt::from_args();
    // eprintln!("{:?}", opt);
    
    let mut instream: Box<dyn std::io::Read> = match &opt.seqs {
        Some(path) => Box::new(File::open(path).unwrap()),
        None => Box::new(io::stdin()),
    };
    let mut outstream: Box<dyn std::io::Write> = match &opt.outfile {
        Some(path) => Box::new(File::open(path).unwrap()),
        None => Box::new(io::stdout()),
    };
    let mut rng: Box<dyn RngCore> = match opt.seed {
        Some(seed) => Box::new(XorShiftRng::seed_from_u64(seed)),
        None => Box::new(rand::thread_rng()),
    };
    
    let size = opt.num_reads;
    let mut reservoir: Vec<fastq::Record> = Vec::new();
    let reader = fastq::Reader::new(instream);
    let mut writer = fastq::Writer::new(outstream);
    let mut count = 0;
    for result in reader.records() {
        let record = result.expect("Error during Fastq parsing");
        count += 1;
        if reservoir.len() < size {
            reservoir.push(record);
        } else {
            let r = rng.gen_range(1, count);
            if r <= size {
                reservoir[r - 1] = record;
            }
        }
    }
    eprintln!(
        "Sampled {} reads from a total of {}",
        reservoir.len(),
        count
    );
    for record in &reservoir {
        writer
            .write_record(record)
            .expect("Error writing Fastq record");
    }
}