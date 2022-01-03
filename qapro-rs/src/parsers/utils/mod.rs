use std::collections::HashSet;

pub fn split_parent_children(sss_org: Vec<Vec<String>>) -> (Vec<String>, Vec<Vec<String>>) {
    let mut sss = sss_org.clone();
    let mut common = Vec::<String>::new();
    'a: loop {
        let mut set = HashSet::<String>::new();
        let mut vec = Vec::<Vec<String>>::new();
        for ss in sss.into_iter() {
            if let Some((first, tail)) = ss.split_first() {
                set.insert(first.to_string());
                vec.push(tail.to_vec());
            } else {
                break 'a;
            }
            if set.len() > 1 {
                break 'a;
            };
        }
        if let Some(s) = set.iter().next() {
            common.push(s.to_string());
        } else {
            break 'a;
        }
        sss = vec;
    }

    let n = common.len();
    let rest_sss = sss_org
        .into_iter()
        .map(|ss| {
            let (_, right) = ss.split_at(n);
            right.to_owned()
        })
        .collect::<Vec<_>>();
    (common, rest_sss)
}

#[cfg(test)]
mod tests {
    use super::split_parent_children;

    #[test]
    fn eq() {
        let ss0 = vec!["hr".to_owned(), "employeesNest".to_owned(), "id".to_owned()];
        let ss1 = vec![
            "hr".to_owned(),
            "employeesNest".to_owned(),
            "name".to_owned(),
        ];
        let ss2 = vec![
            "hr".to_owned(),
            "employeesNest".to_owned(),
            "projects".to_owned(),
            "name".to_owned(),
        ];

        let res = split_parent_children(vec![ss0, ss1, ss2]);
        assert_eq!(
            res,
            (
                vec!["hr".to_owned(), "employeesNest".to_owned(),],
                vec![
                    vec!["id".to_owned(),],
                    vec!["name".to_owned(),],
                    vec!["projects".to_owned(), "name".to_owned(),],
                ]
            )
        );
    }
}
