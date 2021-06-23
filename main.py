# This is a sample Python script.
import src.src as src
import time


def run(source, target):
    if target.get_state() is src.State.NOT_STARTED:
        target.set_state(src.State.RUNNING)
        time.sleep(80)  # Simulate running migration


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    workload = src.Workload()
    workload.set_ip(123)
    workload.create_credentials("FooBar", "encrypted_password", "http://foo.bar.ru")
    workload.add_to_storage(src.MountPoint("D:\\foo\\bar", 102))
    workload.add_to_storage(src.MountPoint("C:\\foo\\bar", 301))
    run(src.Source("FooBar", "encrypted_password", 1230), src.MigrationTarget(workload))
