function deleteColl(collId) {
    fetch("/delete-coll", {
      method: "POST",
      body: JSON.stringify({ collId: collId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }
  function deleteCard(cardlId, collid) {
    fetch("/delete-card", {
      method: "POST",
      body: JSON.stringify({ cardlId: cardlId }),
    }).then((_res) => {
      window.location.href = "/edit-collection/" + collid;
    });
  }