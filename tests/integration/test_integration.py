import requests
import os
import subprocess
import time

def test_integration():
    try:
        images = subprocess.run(["docker ps"], shell=True, check=True, capture_output=True)
        assert "pipeline-in-a-box-web" in images.stdout.decode()
        assert "pipeline-in-a-box-worker" in images.stdout.decode()

        url = "http://localhost:5000/process"
        test_file_path = "tests/files/sample_dna.txt"
        with open(test_file_path, "rb") as f:
            files = {"file": (os.path.basename(test_file_path), f)}
            response = requests.post(url, files=files)
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        task_id = data["task_id"]   
        result_url = f"http://localhost:5000/result/{task_id}"
        for _ in range(10):
            result_response = requests.get(result_url)
            assert result_response.status_code == 200
            result_data = result_response.json()
            if result_data["status"] == "success":
                assert "result" in result_data
                assert result_data["result"]["counts"]["A"] == 15
                assert result_data["result"]["counts"]["T"] == 15
                assert result_data["result"]["counts"]["C"] == 15
                assert result_data["result"]["counts"]["G"] == 15
                break
            elif result_data["status"] == "failed":
                assert False, f"Task failed with error: {result_data['error']}"
            else:
                time.sleep(1)
        else:
            assert False, "Task did not complete within expected time"
    except Exception as e:
        assert False, f"Integration test failed: {str(e)}"