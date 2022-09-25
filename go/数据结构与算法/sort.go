package main

import "fmt"

func insertSort(nums []int) {
	//直接插入排序
	for i := 1; i < len(nums); i++ {
		toInsertNum := nums[i]
		var j int
		for j = i - 1; j >= 0 && toInsertNum < nums[j]; j-- {
			nums[j+1] = nums[j]
		}
		nums[j+1] = toInsertNum
	}
}

func insertSort2(nums []int) {
	//折半插入排序
	for i := 1; i < len(nums); i++ {
		toInsertNum := nums[i]
		low, high := 0, i-1
		for low <= high {
			mid := (low + high) / 2
			midNum := nums[mid]
			if toInsertNum < midNum {
				high = mid - 1
			} else {
				low = mid + 1
			}
		} //寻找插入位置
		for j := i - 1; j >= high+1; j-- {
			nums[j+1] = nums[j]
		} //移动元素
		nums[high+1] = toInsertNum //插入到正常位置
	}
}

func bubbleSort(nums []int) {
	//冒泡排序
	for i := 1; i < len(nums); i++ {
		flag := true
		for j := 0; j < len(nums)-i; j++ {
			if nums[j] > nums[j+1] {
				flag = false
				nums[j], nums[j+1] = nums[j+1], nums[j]
			}
		}
		if flag {
			break
		}
	}
}

func partition(nums []int, low, high int) int {
	//选取枢轴元素，以其作为中轴将其它元素左右归边，返回枢轴元素位置
	x := nums[low]
	for low < high {
		for low < high && nums[high] >= x {
			high--
		}
		nums[low] = nums[high]

		for low < high && nums[low] <= x {
			low++
		}
		nums[high] = nums[low]
	}
	nums[low] = x
	return low
}

func quickSort(nums []int, low, high int) {
	//快速排序
	if low < high {
		pivotloc := partition(nums, low, high) //确定枢轴元素位置
		quickSort(nums, low, pivotloc-1)       //对低子表递归排序
		quickSort(nums, pivotloc+1, high)      //对高子表递归排序
	}
}

func selectSort(nums []int) {
	//简单选择排序
	for i := 0; i < len(nums)-1; i++ {
		minIndex := i
		for j := i + 1; j < len(nums); j++ {
			if nums[j] < nums[minIndex] {
				minIndex = j
			}
		}
		nums[i], nums[minIndex] = nums[minIndex], nums[i]
	}
}

func main() {
	nums := []int{58, 33, 235, 29, 67, 11}
	selectSort(nums)
	fmt.Println(nums)
}

