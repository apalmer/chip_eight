using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.Routing;
using Playground.BusinessLogic;

namespace Playground.Controllers
{
    public class EmployeeSearchController : Controller
    {
        [AcceptVerbs(HttpVerbs.Get)]
        public ActionResult Index()
        {
            var model = new Playground.Models.EmployeeSearchModel();
            return View(model);
        }

        [AcceptVerbs(HttpVerbs.Post)]
        public ActionResult Index(Playground.Models.EmployeeSearchModel model)
        {
            if (!model.Criteria.Validate())
            {
                return View(model);
            }
            else
            {
                return RedirectToAction(
                    "Results", 
                    new{
                        FirstName = model.Criteria.FirstName,
                        LastName = model.Criteria.LastName,
                        Organization = model.Criteria.Organization,
                        JobTitle = model.Criteria.JobTitle,
                        Address = model.Criteria.Address,
                        City = model.Criteria.City,
                        State = model.Criteria.State,
                        ZipCode = model.Criteria.ZipCode
                    }
                );
            }
        }

        public ActionResult Results(Playground.BusinessLogic.EmployeeSearchCriteria searchCriteria)
        {
            if (searchCriteria.Validate())
            {
                //searchCriteria.PageNumber = searchCriteria.PageNumber  ?? 1;
                //searchCriteria.RecordsPerPage = searchCriteria.RecordsPerPage ?? 20;
                var model = new Playground.Models.EmployeeSearchResultsModel();
                var search = new Playground.BusinessLogic.EmployeeSearch();
                model.SearchResults = search.Search(searchCriteria);
                model.Criteria = searchCriteria;
                return View(model);
            }
            else
            {
               return RedirectToAction("Index");
            }
        }
    }
}
