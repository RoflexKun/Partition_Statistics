from partition_statistics import PartitionStatistics

if __name__ == '__main__':
    user_input = input("Please enter a partition letter: ")

    PartitionStatistics(user_input).get_partition_statistics()