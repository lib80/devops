package utils

import "sync"

//实现一个并发安全的set，元素是string

type SafeSet struct {
    sync.RWMutex
    data map[string]struct{}
}

func NewSet() *SafeSet {
    return &SafeSet{
        RWMutex: sync.RWMutex{},
        data: make(map[string]struct{}),
    }
}

func (ss *SafeSet) JudgeElement(key string) bool {
    ss.RLock()
    defer ss.RUnlock()
    _, ok := ss.data[key]
    return ok
}

func (ss *SafeSet) Add(key string) {
    ss.Lock()
    defer ss.Unlock()
    ss.data[key] = struct{}{}
}

func (ss *SafeSet) Del(key string) {
    ss.Lock()
    defer ss.Unlock()
    delete(ss.data, key)
}

func (ss *SafeSet) PrintElement() []string {
    keys := make([]string, 0)
    ss.RLock()
    defer ss.RUnlock()
    for k := range ss.data {
        keys = append(keys, k)
    }
    return keys
}

func (ss *SafeSet) Merge(set *SafeSet) {
    ss.Lock()
    defer ss.Unlock()
    keys := set.PrintElement()
    for _, k := range keys {
        ss.data[k] = struct{}{}
    }
}
