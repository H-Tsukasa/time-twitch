from fastapi.testclient import TestClient

from ..main import app
from ..models import Video

client = TestClient(app)

def test_read_videos(test_db):
    
    video1 = Video(
        date="12-00", 
        title="video",
        duration="12m2s",
        video_number="123",
        view_count="3000",
        thumbnail_url="http",
        embed_url="http",
        streamer_id=1
    )
    video2 = Video(
        date="12-00", 
        title="video2",
        duration="13m2s",
        video_number="1234",
        view_count="3000",
        thumbnail_url="http",
        embed_url="http",
        streamer_id=2
    )

    test_db.add_all([video1, video2])
    test_db.flush()
    test_db.commit()

    # テスト対象の処理を実行
    response = client.get("/api/videos/")

    # 処理の結果の確認
    assert response.status_code == 200
    assert len(response.json()) > 0
    expected_data = [
        {   
            "date": "12-00", 
            "title": "video",
            "duration": "12m2s",
            "video_number": "123",
            "view_count": "3000",
            "thumbnail_url": "http",
            "embed_url": "http",
            "streamer_id": 1
        },
        {        
            "date": "12-00", 
            "title": "video2",
            "duration": "13m2s",
            "video_number": "1234",
            "view_count": "3000",
            "thumbnail_url": "http",
            "embed_url": "http",
            "streamer_id": 2
        },
    ]
    
    for actual, expected in zip(response.json(), expected_data):
        actual_set = set(actual.keys())
        actual_set.remove("id")  # idを除去
        assert actual_set == set(expected.keys())
        assert all(str(actual[key]) == str(expected[key]) for key in actual_set)
        
    # デバッグ用にデータベースの状態を出力
    # print("Database state after test_read_videos:")
    # for video in test_db.query(Video).all():
    #     print(video)


def test_read_videos_by_streamer_id(test_db):
    video1 = Video(
        date="12-00", 
        title="video",
        duration="12m2s",
        video_number="123",
        view_count="3000",
        thumbnail_url="http",
        embed_url="http",
        streamer_id=1
    )
    video2 = Video(
        date="12-00", 
        title="video2",
        duration="13m2s",
        video_number="1234",
        view_count="3000",
        thumbnail_url="http",
        embed_url="http",
        streamer_id=2
    )
    test_db.add_all([video1, video2])
    # test_db.flush()
    test_db.commit()
    
    streamer_id = 1

    with TestClient(app) as new_client:
        response = new_client.get(f"/api/videos/{streamer_id}")

    # 処理の結果の確認
    assert response.status_code == 200
    assert len(response.json()) > 0
    expected_data = [
        {   
            "date": "12-00", 
            "title": "video",
            "duration": "12m2s",
            "video_number": "123",
            "view_count": "3000",
            "thumbnail_url": "http",
            "embed_url": "http",
            "streamer_id": 1
        },
    ]
    
    print("ここだよ")
    print(response.json())
    for actual, expected in zip(response.json(), expected_data):
        actual_set = set(actual.keys())
        actual_set.remove("id")  # idを除去
        print(actual_set)
        assert actual_set == set(expected.keys())
        assert all(str(actual[key]) == str(expected[key]) for key in actual_set)
    # デバッグ用にデータベースの状態を出力
    # print("Database state after test_read_videos:")
    # for video in test_db.query(Video).all():
    #     print(video)
