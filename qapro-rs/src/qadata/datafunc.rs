use std::cmp::PartialOrd;
use std::f64::INFINITY;

/// 存出历史bar队列
#[derive(Debug, Clone)]
pub struct Que<T> {
    q: Vec<T>,
    maxsize: usize,
}

impl<T: Clone> Que<T> {
    pub fn new(maxsize: usize, fill: T) -> Que<T> {
        Que {
            q: vec![fill; maxsize],
            maxsize,
        }
    }
    /// 判断是否为空
    pub fn full(&self) -> bool {
        if self.maxsize == self.q.len() {
            return true;
        }
        false
    }

    fn get(&mut self) -> T {
        self.q.remove(0)
    }

    pub fn push(&mut self, data: T) {
        if self.full() {
            self.get();
        }
        self.q.push(data);
    }

    pub fn len(&self) -> usize {
        self.q.len()
    }

    pub fn clear(&mut self) {
        self.q.clear();
    }

    pub fn data(&self) -> &[T] {
        &self.q
    }
    /// 往左偏移
    pub fn shift(&self, step: usize) -> &[T] {
        &self.q[..self.len() - step]
    }

    /// 最后几项，可先偏移
    pub fn tails(&self, length: usize, shift: usize) -> &[T] {
        match shift {
            0 => {
                if length > self.len() {
                    return &self.q;
                }
                return &self.q[self.len() - length..];
            }
            _ => {
                let x = self.shift(shift);
                if length > x.len() {
                    return x;
                }
                return &x[x.len() - length..];
            }
        }
    }
    /// 最后一项，可先偏移
    pub fn tail(&self, shift: usize) -> &T {
        match shift {
            0 => {
                return self.q.last().unwrap();
            }
            _ => {
                let x = self.shift(shift);
                return x.last().unwrap();
            }
        }
    }
    /// 更新最后一个值
    pub fn last_update(&mut self, data: T) {
        if let Some(x) = self.q.last_mut() {
            *x = data;
        }
    }
}

/// 取队列中的最大值
pub fn dhhv(lst: &[f64], tail: usize) -> f64 {
    let mut max = -INFINITY;
    let l = lst.len();
    let x = if tail > l { lst } else { &lst[l - tail..] };
    for i in x {
        if i > &max {
            max = *i;
        }
    }
    return max;
}

/// 取队列中的最小值
pub fn dllv(lst: &[f64], tail: usize) -> f64 {
    let mut min = INFINITY;
    let l = lst.len();
    let x = if tail > l { lst } else { &lst[l - tail..] };
    for i in x {
        if i < &min {
            min = *i;
        }
    }
    return min;
}

pub fn dma(lst: &[f64], tail: usize) -> f64 {
    let l = lst.len();
    let mut res = 0.0;
    if l <= tail {
        for i in lst {
            res += *i;
        }
        return res / l as f64;
    } else {
        for i in &lst[l - tail..l] {
            res += *i;
        }
        return res / tail as f64;
    }
}

/// 两值最大值
pub fn max<T: PartialOrd>(a: T, b: T) -> T {
    if a > b {
        a
    } else {
        b
    }
}

/// 两值最小值
pub fn min<T: PartialOrd>(a: T, b: T) -> T {
    if a < b {
        a
    } else {
        b
    }
}

/// 数字的最大值
pub fn vec_maximum(lst: &[f64], tail: usize) -> f64 {
    match tail {
        0 => {
            let mut max = -INFINITY;
            for i in lst {
                if i > &max {
                    max = *i;
                }
            }
            return max;
        }
        _ => {
            let mut max = -INFINITY;
            let l = lst.len();
            let x = if tail > l { lst } else { &lst[l - tail..] };
            for i in x {
                if i > &max {
                    max = *i;
                }
            }
            return max;
        }
    }
}

/// 数组中的最小值
pub fn vec_minimum(lst: &[f64], tail: usize) -> f64 {
    match tail {
        0 => {
            let mut min = INFINITY;
            for i in lst {
                if i < &min {
                    min = *i;
                }
            }
            min
        }
        _ => {
            let mut min = INFINITY;
            let l = lst.len();
            let x = if tail > l { lst } else { &lst[l - tail..] };
            for i in x {
                if i < &min {
                    min = *i;
                }
            }
            return min;
        }
    }
}

/// 取两数组每项的较大值
pub fn vec_bigger(a: &[f64], b: &[f64]) -> Vec<f64> {
    // 以长度较短的为主干，木桶效应,且右对齐
    let al = a.len();
    let bl = b.len();
    let mut res = Vec::new();
    let h = min(al, bl);
    let a1 = &a[al - h..];
    let b1 = &b[bl - h..];
    for (index, i) in a1.iter().enumerate() {
        let t = &b1[index];
        if i > t {
            res.push(*i);
        } else {
            res.push(*t);
        }
    }
    res
}

/// 取两数组每项的较小值
pub fn vec_smaller(a: &[f64], b: &[f64]) -> Vec<f64> {
    // 以长度较短的为主干，木桶效应,且右对齐
    let al = a.len();
    let bl = b.len();
    let mut res = Vec::new();
    let h = min(al, bl);
    let a1 = &a[al - h..];
    let b1 = &b[bl - h..];
    for (index, i) in a1.iter().enumerate() {
        let t = &b1[index];
        if i < t {
            res.push(*i);
        } else {
            res.push(*t);
        }
    }
    res
}

/// 两数组的差值，可设定abs
pub fn diff(a: &[f64], b: &[f64], abs: bool) -> Vec<f64> {
    // 以长度较短的为主干，木桶效应,且右对齐
    let al = a.len();
    let bl = b.len();
    let mut res = Vec::new();
    let h = min(al, bl);
    let a1 = &a[al - h..];
    let b1 = &b[bl - h..];
    for (index, v) in a1.iter().enumerate() {
        let si = if abs {
            (v - b1[index]).abs()
        } else {
            v - b1[index]
        };
        res.push(si);
    }
    res
}

/// a 中 大于 b 的个数
pub fn vec_gt_count(a: &[f64], b: &[f64]) -> usize {
    let al = a.len();
    let bl = b.len();
    let mut count = 0;
    let h = min(al, bl);
    let a1 = &a[al - h..];
    let b1 = &b[bl - h..];
    for (index, i) in a1.iter().enumerate() {
        if i > &b1[index] {
            count += 1;
        }
    }
    count
}

/// 获取a 中 大于b 的bool值
pub fn vec_gt_bool(a: &[f64], b: f64) -> Vec<bool> {
    let mut res = Vec::new();
    for i in a {
        if i > &b {
            res.push(true);
        } else {
            res.push(false);
        }
    }
    res
}

/// 获取a 中 大于等于b 的bool值
pub fn vec_gte_bool(a: &[f64], b: f64) -> Vec<bool> {
    let mut res = Vec::new();
    for i in a {
        if i >= &b {
            res.push(true);
        } else {
            res.push(false);
        }
    }
    res
}
