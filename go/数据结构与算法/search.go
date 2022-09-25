package main

import "fmt"

func binarySearch(nums []int, n int) int {
	//二分查找
	low, high := 0, len(nums)-1
	for low <= high {
		mid := (low + high) / 2
		midNum := nums[mid]
		if n == midNum {
			fmt.Println("查找成功")
			return mid
		} else if n < midNum {
			high = mid - 1
		} else {
			low = mid + 1
		}
	}
	return -1
}

func binarySearch2(nums []int, n, low, high int) int {
	//二分查找：递归写法
	if low > high {
		return -1
	}
	mid := (low + high) / 2
	midNum := nums[mid]
	if n == midNum {
		return mid
	} else if n < midNum {
		return binarySearch2(nums, n, low, mid-1)
	} else {
		return binarySearch2(nums, n, mid+1, high)
	}

}

func main() {
	index := binarySearch([]int{33, 9, 3, 88, 11}, 88)
	fmt.Println(index)
}

