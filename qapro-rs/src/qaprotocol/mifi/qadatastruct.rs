use std::collections::BTreeMap;

#[derive(Debug)]
struct Movie {
    name: &'static str,
    year: i32,
    rating: i32,
}

#[derive(Debug)]
struct MovieDb<'a> {
    by_year: BTreeMap<i32, Vec<&'a Movie>>,
    by_rating: BTreeMap<i32, Vec<&'a Movie>>,
}

impl <'a> MovieDb <'a> {
    fn get_first_by_year(&'a self, year: i32) -> &'a Movie {
        let index = &self.by_year[&year];
        // TODO: Error handling.
        &*index.first().unwrap()
    }
}

fn build_movie_db<'a>(list: &'a Vec<Movie>) -> MovieDb<'a> {

    let mut by_year = BTreeMap::new();
    let mut by_rating = BTreeMap::new();
    for m in list.iter() {
        by_year.entry(m.year).or_insert(vec![]).push(&*m);
        by_rating.entry(m.rating).or_insert(vec![]).push(&*m);
    }

    MovieDb{by_year: by_year, by_rating: by_rating}
}

fn main() {
    let list = vec![
        Movie{name: "The Thing", year: 1982, rating: 9},
        Movie{name: "The Matrix", year: 1999, rating: 10},
        Movie{name: "Memento", year: 2000, rating: 8},
        Movie{name: "Alien", year: 1979, rating: 9},
    ];

    let db = build_movie_db(&list);
    println!("{:?}", db);

    let m1 = db.get_first_by_year(1999);
    println!("{:?}", m1);

    let m2 = db.get_first_by_year(1982);
    println!("{:?}", m2);

    let m3 = db.get_first_by_year(1999);
    println!("{:?}", m3);
}