import subprocess
import collections

ScanResult = collections.namedtuple("ScanResult", ["MAC", "name"])

def do_scan():
	p = subprocess.run(["hcitool", "scan"], capture_output=True)
	lines = p.stdout.decode().splitlines()
	result_lines = p.stdout.decode().splitlines()[1:]
	results = []
	for result in result_lines:
		result_parts = result.strip().split("\t")
		results.append(ScanResult(result_parts[0], result_parts[1]))
	return results


if __name__ == "__main__":
	results = do_scan()
	if len(results):
		for r in results:
			print("{} {}".format(r.MAC, r.name))
	else:
		print("No results")
